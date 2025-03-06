<template>
    <div>
        <q-page>
            <div class="q-pb-md q-pt-md q-pl-md" style="  font-size: 24px;">
                <b>Check-in</b>
            </div>
            <q-select filled v-model="selectedEvent" :options="events" label="Select Event" emit-value map-options
                @input="fetchCheckins" />
            <q-table :rows="checkins" :columns="columns" row-key="id" :loading="loading"
                no-data-label="No check-ins available">
                <template v-slot:top-right>
                    <q-btn color="primary" label="Refresh" @click="fetchCheckins" :disable="!selectedEvent"
                        icon="refresh" />
                </template>
            </q-table>
            <q-banner v-if="errorMessage" class="bg-negative text-white">
                <q-icon name="error" size="xs" />
                {{ errorMessage }}
            </q-banner>
        </q-page>
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

        const tab = ref<string>("Check-in");

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
            goToAudiences
        };
    },
});
</script>