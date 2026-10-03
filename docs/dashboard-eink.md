# E-ink household dashboard

## Goal

Portrait wall/entry dashboard with a black-picture-frame aesthetic, battery, Wi-Fi, and preferably full-surface touch.

Desired widgets/actions:

- weather
- shared Google Calendar / today
- shopping list with add/check interaction
- messages sent remotely to the household display
- Home Assistant scenes/buttons
- temperatures, tasks, reminders, possibly news

## Hardware direction

Current pragmatic favorite: Seeed Studio reTerminal E1003 (10.3-inch monochrome e-paper + touch).

Desired future hardware: approximately 13.3-inch monochrome/greyscale e-paper with capacitive touch, battery, Wi-Fi, and a clean black frame.

Seeed E1004 was considered but is not preferred for this control-panel use because it lacks touch and has slower color refresh behavior.

## Software direction

Keep the UI hardware-independent. Home Assistant should remain the canonical backend for state/actions. Prototype the portrait UI in a browser before committing to display hardware. Tesserae, ESPHome, or a custom UI are possible implementation layers.
