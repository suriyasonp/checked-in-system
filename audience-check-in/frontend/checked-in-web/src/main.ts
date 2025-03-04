import { createApp } from "vue";
import App from "./App.vue";
import quasar from "./plugins/quasar";

const app = createApp(App);

// Add Quasar
quasar(app);

app.mount("#app");