import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

loader = importlib.machinery.SourceFileLoader('audio', str(Path(__file__).resolve().parents[1] / 'audio/bin/homepi-audio'))
spec = importlib.util.spec_from_loader(loader.name, loader)
audio = importlib.util.module_from_spec(spec)
loader.exec_module(audio)


def info():
    return {'streams': [
        {'codec_type': 'video', 'codec_name': 'hevc', 'width': 1920, 'height': 1080, 'pix_fmt': 'yuv420p10le'},
        {'codec_type': 'audio', 'codec_name': 'truehd', 'channels': 6, 'tags': {'language': 'eng'}},
        {'codec_type': 'audio', 'codec_name': 'truehd', 'channels': 2, 'tags': {'language': 'jpn'}},
        {'codec_type': 'subtitle', 'codec_name': 'ass', 'tags': {'language': 'eng'}}],
        'format': {'duration': '1500'}, 'chapters': [{'id': 1}]}


class Tests(unittest.TestCase):
    def test_plan_replaces_truehd_and_copies_other_streams(self):
        args, count = audio.ffmpeg_args(info())
        self.assertEqual(count, 2)
        self.assertEqual(args[:4], ['-map', '0', '-c', 'copy'])
        self.assertIn('-c:a:0', args)
        self.assertIn('-c:a:1', args)
        self.assertNotIn('-c:v', args)

    def test_no_truehd_no_conversion(self):
        source = info()
        for s in source['streams'][1:3]:
            s['codec_name'] = 'ac3'
        self.assertEqual(audio.ffmpeg_args(source)[1], 0)

    def test_71_explicitly_downmixes_to_51(self):
        source = info()
        source['streams'][1]['channels'] = 8
        args, _ = audio.ffmpeg_args(source)
        self.assertEqual(args[args.index('-ac:a:0')+1], '6')

    def test_unknown_layout_refused(self):
        source = info()
        source['streams'][1]['channels'] = 3
        with self.assertRaises(ValueError):
            audio.ffmpeg_args(source)

    def test_validation_detects_lost_subtitles_and_video_changes(self):
        before = info()
        after = copy.deepcopy(before)
        for s in after['streams'][1:3]:
            s['codec_name'] = 'ac3'
        media = Mock()
        media.video_hash.return_value = 'SHA256=example'
        audio.verify(before, after, media, Path('old'), Path('new'))
        after['streams'].pop()
        with self.assertRaises(ValueError):
            audio.verify(before, after, media, Path('old'), Path('new'))
        after = copy.deepcopy(before)
        for s in after['streams'][1:3]:
            s['codec_name'] = 'ac3'
        media.video_hash.side_effect = ['SHA256=old', 'SHA256=new']
        with self.assertRaises(ValueError):
            audio.verify(before, after, media, Path('old'), Path('new'))

    def test_hardlink_archive_and_torrent_survive_atomic_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, result, torrent = root/'source.mkv', root/'result.mkv', root/'torrent.mkv'
            source.write_bytes(b'original')
            audio.os.link(source, torrent)
            expected = audio.fingerprint(source)
            result.write_bytes(b'converted')
            entry = audio.archive_and_replace(source, result, expected, root/'archive')
            self.assertEqual(source.read_bytes(), b'converted')
            self.assertEqual(torrent.read_bytes(), b'original')
            self.assertEqual((entry/'original.mkv').read_bytes(), b'original')
            self.assertNotEqual(source.stat().st_ino, torrent.stat().st_ino)
            self.assertEqual(json.loads((entry/'manifest.json').read_text())['status'], 'replaced')

    def test_changed_source_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, result = root/'source.mkv', root/'result.mkv'
            source.write_bytes(b'old')
            expected = audio.fingerprint(source)
            source.write_bytes(b'new content')
            result.write_bytes(b'converted')
            with self.assertRaises(ValueError):
                audio.archive_and_replace(source, result, expected, root/'archive')
            self.assertEqual(source.read_bytes(), b'new content')

    def test_symlink_or_outside_input_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root/'media'
            media.mkdir()
            source = media/'source.mkv'
            source.write_bytes(b'original')
            link = media/'link.mkv'
            link.symlink_to(source)
            with self.assertRaises(ValueError):
                audio.checked_source(link, (media,))
            with self.assertRaises(ValueError):
                audio.checked_source(root/'outside.mkv', (media,))

    def test_playing_session_does_not_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'source.mkv'
            source.write_bytes(b'original')
            media, jf = Mock(), Mock()
            jf.idle.return_value = False
            self.assertFalse(audio.process(source, media, jf))
            media.convert.assert_not_called()
            self.assertEqual(source.read_bytes(), b'original')

    def test_playback_started_during_job_defers_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'source.mkv'
            source.write_bytes(b'original')
            media, jf = Mock(), Mock()
            jf.idle.side_effect = [True, False]
            media.probe.return_value = info()
            with patch.object(audio, 'STAGING', root/'staging'), patch.object(audio, 'verify'), patch.object(audio, 'archive_and_replace') as replace:
                self.assertFalse(audio.process(source, media, jf))
                replace.assert_not_called()
            self.assertEqual(source.read_bytes(), b'original')

    def test_conversion_failure_never_replaces_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'source.mkv'
            source.write_bytes(b'original')
            media, jf = Mock(), Mock()
            jf.idle.return_value = True
            media.probe.return_value = info()
            media.convert.side_effect = RuntimeError('simulated encode failure')
            with patch.object(audio, 'STAGING', root/'staging'), patch.object(audio, 'archive_and_replace') as replace:
                with self.assertRaises(RuntimeError):
                    audio.process(source, media, jf)
                replace.assert_not_called()
            self.assertEqual(source.read_bytes(), b'original')

    def test_archive_link_failure_preserves_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, result = root/'source.mkv', root/'result.mkv'
            source.write_bytes(b'old')
            result.write_bytes(b'new')
            with patch.object(audio.os, 'link', side_effect=OSError('simulated disk error')):
                with self.assertRaises(OSError):
                    audio.archive_and_replace(source, result, audio.fingerprint(source), root/'archive')
            self.assertEqual(source.read_bytes(), b'old')


if __name__ == '__main__':
    unittest.main()
