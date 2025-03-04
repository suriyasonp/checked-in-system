<template>
  <div id="app" class="q-pa-md">
    <q-layout view="lHh lpr lFf" container style="height: 400px" class="shadow-2 rounded-borders">
      <q-header bordered class="bg-grey-3 text-primary">
        <q-toolbar>
          <!-- <q-btn flat round dense icon="menu" class="q-mr-sm" /> -->
          <q-avatar>
            <img src="./assets/target.png">
          </q-avatar>

          <q-toolbar-title class="text-center text-dark">Audience check-in system</q-toolbar-title>

          <q-btn flat round dense icon="event" />
        </q-toolbar>
      </q-header>

      <q-footer bordered class="bg-grey-3 text-primary">
        <q-tabs no-caps active-color="primary" indicator-color="transparent" class="text-grey-8" v-model="tab">
          <q-tab name="Audiences" label="Audiences" />
          <q-tab name="Check-in" label="Check-in" />
          <q-tab name="About me" label="About me" />
        </q-tabs>
      </q-footer>

      <q-page-container>
      <q-page>
    <!-- Event selection dropdown -->
    <q-select
      filled
      v-model="selectedEvent"
      :options="events"
      label="Select Event"
      emit-value
      map-options
      @input="fetchCheckins"
    />
    
    
    <!-- Table to display check-ins -->
    <q-table
      :rows="checkins"
      :columns="columns"
      row-key="id"
      :loading="loading"
      no-data-label="No check-ins available"
    >
      <template v-slot:top-right>
        <q-btn 
          color="primary" 
          label="Refresh" 
          @click="fetchCheckins" 
          :disable="!selectedEvent"
          icon="refresh" />
      </template>
    </q-table>

    <!-- Display error messages if needed -->
    <q-banner v-if="errorMessage" class="bg-negative text-white">
      <q-icon name="error" size="xs" />
      {{ errorMessage }}
    </q-banner>

  </q-page>
  </q-page-container>
  </q-layout>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getEvents, getCheckins } from './services/api';

export default defineComponent({
  name: 'App',
  setup() {
    const events = ref<any[]>([]);
    const checkins = ref<any[]>([]);
    const selectedEvent = ref<number | null>(null);
    const loading = ref<boolean>(false);
    const errorMessage = ref<string | null>(null);

    const tab = ref<string>("Check-in");

    const columns = [
      { name: 'order', label: '#', align: 'center', field: 'order' },
      { name: 'full_name_th', label: 'Name', align: 'left', field: 'full_name_th' },
      { name: 'full_name_en', label: 'Name English', align: 'left', field: 'full_name_en' },
      { name: 'check_in_time', label: 'Check-in Time', align: 'center', field: 'check_in_time' },
    ];

    const fetchEvents = async () => {
      try {
        const data = await getEvents();
        events.value = data.map((event: any) => ({
          label: event.name,
          value: event.id
        }));
      } catch (error) {
        console.error('Error fetching events', error);
        errorMessage.value = 'Failed to load events. Please try again later.';
      }
    };

    const fetchCheckins = async () => {
      if (!selectedEvent.value) {
        return;
      }

      loading.value = true;
      try {
        const data = await getCheckins(selectedEvent.value);
        checkins.value = data.map((checkin: any, index: number) => ({
          order: index + 1,
          ...checkin,
          full_name_th: checkin.audience.full_name_th,
          full_name_en: checkin.audience.full_name_en,
          check_in_time: new Date(checkin.check_in_time).toLocaleString()
        }));
        errorMessage.value = null; // Clear any previous error
      } catch (error) {
        console.error('Error fetching check-ins', error);
        errorMessage.value = 'Failed to load check-ins. Please try again later.';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchEvents();
    });

    return {
      events,
      checkins,
      selectedEvent,
      loading,
      columns,
      fetchCheckins,
      errorMessage,
      tab
    };
  },
});
</script>

<style scoped>
#app {
  max-width: 1200px;
  margin: 0 auto;
}

.q-select,
.q-table {
  margin-bottom: 20px;
}

.q-banner {
  margin-top: 20px;
}
</style>