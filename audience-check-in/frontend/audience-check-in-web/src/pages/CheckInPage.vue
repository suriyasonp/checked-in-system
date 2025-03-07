<template>
    <div>
        <q-page>
            <div class="q-pb-md q-pt-md q-pl-md" style="font-size: 24px;">
                <b>Check-in</b>
            </div>
            <q-select filled v-model="selectedEvent" :options="events" label="Select Event" emit-value map-options
                @update:model-value="fetchCheckins" />
            <q-table :rows="checkins" :columns="columns" row-key="id" :loading="loading"
                no-data-label="No check-ins available">
                <template v-slot:top-right>
                    <q-btn color="primary" label="Refresh" @click="fetchCheckins" :disable="!selectedEvent"
                        icon="refresh" class="q-mr-sm btn-icon" />
                    <q-btn color="green" label="Check-in" @click="showCheckInModal" icon="check_circle"
                        class="btn-icon" />
                </template>
            </q-table>

            <q-dialog v-model="checkInModal" persistent>
                <q-card style="width: 700px;">
                    <q-card-section>
                        <div class="text-h6">Check-in</div>
                    </q-card-section>
                    <q-card-section>
                        <q-select v-model="selectedCheckInEvent" :options="events" label="Select Event" emit-value
                            map-options @update:model-value="fetchAudienceList" />
                        <q-input v-model="checkInData" label="Enter Full Name" :disable="!selectedCheckInEvent">
                            <template v-slot:append>
                                <q-icon name="search" />
                            </template>
                        </q-input>
                        <q-table v-if="filteredAudienceList.length" :rows="filteredAudienceList"
                            :columns="columnsDialog" row-key="id">
                            <template v-slot:body-cell-full_name_th="props">
                                <q-td :props="props">
                                    <q-radio v-model="selectedAudience" :val="props.row"
                                        @click="selectName(props.row)" />
                                    {{ props.row.full_name_th }}
                                </q-td>
                            </template>
                        </q-table>
                        <q-banner v-if="errorMessageOnDialog" class="bg-negative text-white">
                            <q-icon name="error" size="xs" />
                            {{ errorMessageOnDialog }}
                        </q-banner>
                    </q-card-section>
                    <q-card-actions align="right">
                        <q-btn flat label="Cancel" color="primary" v-close-popup />
                        <q-btn flat label="Check-in" color="primary" @click="performCheckIn" />
                    </q-card-actions>
                </q-card>
            </q-dialog>

            <q-banner v-if="errorMessage" class="bg-negative text-white">
                <q-icon name="error" size="xs" />
                {{ errorMessage }}
            </q-banner>

        </q-page>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import { getEvents, getCheckins, postCheckin, getAudienceByEvent } from '../services/api';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'MainPage',
    setup() {
        const events = ref<any[]>([]);
        const checkins = ref<any[]>([]);
        const selectedEvent = ref<number | null>(null);
        const selectedCheckInEvent = ref<number | null>(null);
        const loading = ref<boolean>(false);
        const errorMessage = ref<string | null>(null);
        const errorMessageOnDialog = ref<string | null>(null);
        const checkInModal = ref<boolean>(false);
        const checkInData = ref<string>('');
        const searchResults = ref<any[]>([]);
        const tAudienceList = ref<any[]>([]);
        const filteredAudienceList = ref<any[]>([]);
        const selectedAudience = ref<any>(null);
        const checkedInAudiences = ref<any[]>([]);
        const audienceId = ref();

        const columnsDialog = [
            { name: 'full_name_th', label: 'Name', align: 'left', field: 'full_name_th' },
        ];

        const columns = [
            { name: 'order', label: '#', align: 'center', field: 'order' },
            { name: 'full_name_th', label: 'Name', align: 'left', field: 'full_name_th' },
            { name: 'nickname_th', label: 'Nickname', align: 'left', field: 'nick_name_th' },
            { name: 'full_name_en', label: 'Name English', align: 'left', field: 'full_name_en' },
            { name: 'nickname_en', label: 'Nickname English', align: 'left', field: 'nick_name_en' },
            { name: 'organization', label: 'Organization', align: 'left', field: 'organization' },
            { name: 'check_in_time', label: 'Check-in Time', align: 'center', field: 'check_in_time' },
        ];

        const filterAudienceList = () => {
            if (checkInData.value) {
                filteredAudienceList.value = tAudienceList.value.filter(audience =>
                    audience.full_name_th.toLowerCase().includes(checkInData.value.toLowerCase())
                );
            } else {
                filteredAudienceList.value = tAudienceList.value;
            }
        };
        watch(checkInData, (newValue) => {
            if (newValue) {
                filterAudienceList();
            }
        });

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

        const fetchAudienceList = async () => {
            if (!selectedCheckInEvent.value) {
                return;
            }

            try {
                const data = await getAudienceByEvent(selectedCheckInEvent.value);
                tAudienceList.value = data;
                const res = await getCheckins(selectedCheckInEvent.value);
                checkedInAudiences.value = res.map((checkin: any, index: number) => ({
                    order: index + 1,
                    ...checkin,
                    full_name_th: checkin.audience.full_name_th,
                    full_name_en: checkin.audience.full_name_en,
                    nick_name_th: checkin.audience.nick_name_th,
                    nick_name_en: checkin.audience.nick_name_en,
                    organization: checkin.audience.organization,
                    check_in_time: new Date(checkin.check_in_time).toLocaleString()
                }));
                filteredAudienceList.value = tAudienceList.value;
            } catch (error) {
                console.error('Error fetching audience list', error);
            }
        };

        const showCheckInModal = () => {
            checkInModal.value = true;
        };

        const selectName = (result: any) => {
            checkInData.value = result.full_name_th;
            audienceId.value = result.id;

            filteredAudienceList.value = [];
        };

        const performCheckIn = async () => {
            if (!selectedCheckInEvent.value || !audienceId.value) {
                errorMessage.value = 'Please select an event and enter a full name.';
                return;
            }

            try {
                const audience = checkedInAudiences.value.find(checkin => checkin.full_name_th === checkInData.value);
                if (audience) {
                    errorMessageOnDialog.value = 'Check-in already exists.';
                    return;
                } else {
                    const requestBody = {
                        audience_id: audienceId.value,
                        event_id: selectedCheckInEvent.value
                    };
                    await postCheckin(requestBody);
                    checkInModal.value = false;
                    fetchCheckins();
                }
            } catch (error) {
                console.error('Error performing check-in', error);
                errorMessage.value = 'Failed to perform check-in. Please try again later.';
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
            selectedCheckInEvent,
            loading,
            columns,
            fetchCheckins,
            errorMessage,
            errorMessageOnDialog,
            checkInModal,
            checkInData,
            searchResults,
            showCheckInModal,
            selectName,
            performCheckIn,
            goToAudiences,
            fetchAudienceList,
            filteredAudienceList,
            filterAudienceList,
            tAudienceList,
            columnsDialog,
            selectedAudience
        };
    },
});
</script>