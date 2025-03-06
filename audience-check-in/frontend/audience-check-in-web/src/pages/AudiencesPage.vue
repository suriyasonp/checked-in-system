<template>
    <div>
        <q-page>
            <q-select filled v-model="selectedEvent" :options="events" label="Select Event" emit-value map-options
                @input="fetchAudiences" />
            <q-table :rows="audiences" :columns="columns" row-key="id" :loading="loading"
                no-data-label="No audiences available">
                <template v-slot:top-right>
                    <q-btn color="primary" label="Refresh" @click="fetchAudiences" :disable="!selectedEvent"
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
import { getEvents, getAudiences } from '../services/api';

export default defineComponent({
    name: 'AudiencesPage',
    setup() {
        const events = ref<any[]>([]);
        const audiences = ref<any[]>([]);
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

        const fetchAudiences = async () => {
            if (!selectedEvent.value) {
                return;
            }

            loading.value = true;
            try {
                const data = await getAudiences(selectedEvent.value);
                audiences.value = data.map((audience: any, index: number) => ({
                    order: index + 1,
                    ...audience,
                    full_name_th: audience.full_name_th,
                    full_name_en: audience.full_name_en,
                    nick_name_th: audience.nick_name_th,
                    nick_name_en: audience.nick_name_en,
                    organization: audience.organization,
                }));
                errorMessage.value = null;
            } catch (error) {
                console.error('Error fetching audiences', error);
                errorMessage.value = 'Failed to load audiences. Please try again later.';
            } finally {
                loading.value = false;
            }
        };
        onMounted(() => {
            fetchEvents();
        });

        return {
            events,
            audiences,
            selectedEvent,
            loading,
            columns,
            fetchAudiences,
            errorMessage,
            tab
        };
    },
});
</script>