<template>
  <div id="app">
    <div>
      <q-btn label="Click Me" color="primary" @click="handleClick" />
      <label for="event-select">Select Event: </label>
      <select v-model="selectedEventId" @change="fetchCheckins">
        <option v-for="event in events" :key="event.id" :value="event.id">
          {{ event.name }}
        </option>
      </select>

      </div>

    <table v-if="checkins.length > 0">
      <thead>
        <tr>
          <th>Audience Name</th>
          <th>Check-in Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="checkin in checkins" :key="checkin.id">
          <td>{{ checkin.audience.full_name_th }}</td>
          <td>{{ convertToLocalTime(checkin.check_in_time) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No check-ins available for this event.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { getEvents, getCheckins } from "./services/api";

export default defineComponent({
  name: "App",
  data() {
    return {
      events: [] as Array<{ id: number; name: string }>, // Event list
      selectedEventId: null as number | null, // Selected event ID
      checkins: [] as Array<{
        id: number;
        audience: { full_name_th: string };
        check_in_time: string;
      }>, // Check-in list
    };
  },
  methods: {
    handleClick() {
      alert("Quasar Button Clicked!");
    },

    async fetchEventsData() {
      try {
        this.events = await getEvents();
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    },

    async fetchCheckins() {
      if (this.selectedEventId !== null) {
        try {
          this.checkins = await getCheckins(this.selectedEventId);
        } catch (error) {
          console.error("Error fetching check-ins:", error);
        }
      }
    },

    convertToLocalTime(utcTime: string): string {
      const localDate = new Date(utcTime); // Convert to Date object
      return localDate.toLocaleString(); // Converts to local time string based on browser locale
    },
  },
  mounted() {
    this.fetchEventsData(); // Fetch events on page load
  },
});
</script>

<style scoped>
/* Add some basic styles here */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
}
</style>
