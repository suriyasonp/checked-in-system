<template>
  <div id="app" >
    <q-layout view="lHh lpr lFf" container style="min-height: 100vh; height: auto;" class="shadow-2 rounded-borders">

      <q-header bordered class="bg-grey-3 text-primary">
        <q-toolbar>
          <q-avatar>
            <img src="../assets/target.png">
          </q-avatar>
          <q-toolbar-title class="text-center text-dark">Audience check-in system</q-toolbar-title>
          <q-btn flat round dense icon="event" />
        </q-toolbar>
      </q-header>

      <q-footer bordered class="bg-grey-3 text-primary">
        <q-tabs no-caps active-color="primary" indicator-color="transparent" class="text-grey-8" v-model="tab">
          <q-tab name="Home" label="Home" @click="goToHome" />
          <q-tab name="Audiences" label="Audiences" @click="goToAudiences" />
          <q-tab name="Check-in" label="Check-in" />
          <q-tab name="Register" label="Register" @click="goToRegister" />
        </q-tabs>
      </q-footer>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getEvents, getCheckins } from '../services/api';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MainPage',
  setup() {
    const events = ref<any[]>([]);
    const checkins = ref<any[]>([]);
    const selectedEvent = ref<number | null>(null);
    const loading = ref<boolean>(false);
    const errorMessage = ref<string | null>(null);

    const tab = ref<string>("Home");

    const columns = [
      { name: 'order', label: '#', align: 'center', field: 'order' },
      { name: 'full_name_th', label: 'Name', align: 'left', field: 'full_name_th' },
      { name: 'nickname_th', label: 'Nickname', align: 'left', field: 'nick_name_th' },
      { name: 'full_name_en', label: 'Name English', align: 'left', field: 'full_name_en' },
      { name: 'nickname_en', label: 'Nickname English', align: 'left', field: 'nick_name_en' },
      { name: 'organization', label: 'Organization', align: 'left', field: 'organization' },
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
          nick_name_th: checkin.audience.nick_name_th,
          nick_name_en: checkin.audience.nick_name_en,
          organization: checkin.audience.organization,
          check_in_time: new Date(checkin.check_in_time).toLocaleString()
        }));
        errorMessage.value = null;
      } catch (error) {
        console.error('Error fetching check-ins', error);
        errorMessage.value = 'Failed to load check-ins. Please try again later.';
      } finally {
        loading.value = false;
      }
    };
    const router = useRouter();

    const goToAudiences = () => {
      router.push('/audiences');
    };

    const goToHome = () => {
      router.push('/');
    };

    const goToRegister = () => {
      router.push('/register');
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
      tab,
      goToAudiences,
      goToHome,
      goToRegister
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
