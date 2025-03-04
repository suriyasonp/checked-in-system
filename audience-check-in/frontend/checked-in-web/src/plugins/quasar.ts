// src/plugins/quasar.ts
import { createApp } from "vue";
import { Quasar } from "quasar";
import "@quasar/extras/material-icons/material-icons.css";  // Optional, for icons
import "quasar/dist/quasar.css";  // Import Quasar CSS

export default (app: ReturnType<typeof createApp>) => {
    app.use(Quasar);
};