<template>
    <q-page>
        <q-form @submit="onSubmit" @reset="onReset">
            <div class="q-pb-md q-pt-md" style="  font-size: 24px;">
                <b>Register</b>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.full_name_th" label="Full Name (TH)" filled />
                </div>
                <div class="col">
                    <q-input v-model="form.full_name_en" label="Full Name (EN)" filled />
                </div>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.nick_name_th" label="Nickname (TH)" filled />
                </div>
                <div class="col">
                    <q-input v-model="form.nick_name_en" label="Nickname (EN)" filled />
                </div>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.email" label="Email" type="email" filled />
                </div>
                <div class="col">
                    <q-input v-model="form.phone" label="Phone" type="tel" filled />
                </div>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.organization" label="Organization" filled />
                </div>
                <div class="col">
                    <q-input v-model="form.occupation" label="Occupation" filled />
                </div>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.year_grade" label="Year Grade" filled />
                </div>
                <div class="col">
                    <q-input v-model="form.faculty" label="Faculty" filled />
                </div>
            </div>
            <div class="row q-mb-md">
                <div class="col q-mr-md">
                    <q-input v-model="form.department" label="Department" filled />
                </div>
                <div class="col">
                    <q-select filled v-model="form.event_id" :options="events" label="Select Event" emit-value
                        map-options />
                </div>
            </div>
            <div class="q-mt-md row justify-end">
                <q-btn label="Cancel" type="reset" color="grey" class="q-mr-sm btn" reset />
                <q-btn label="Save" type="submit" color="primary" class="btn" />
            </div>
        </q-form>
    </q-page>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { registerAudience, getEvents } from '../services/api';

export default defineComponent({
    name: 'RegisterPage',
    setup() {
        const events = ref<any[]>([]);
        const errorMessage = ref<string | null>(null);

        const form = ref({
            full_name_th: '',
            full_name_en: '',
            nick_name_th: '',
            nick_name_en: '',
            email: '',
            phone: '',
            organization: '',
            occupation: '',
            year_grade: 0,
            faculty: '',
            department: '',
            event_id: [],
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

        const onSubmit = async () => {
            try {
                const response = await registerAudience(form.value);
                console.log('Form submitted:', response);
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        };

        const onReset = () => {
            form.value = {
                full_name_th: '',
                full_name_en: '',
                nick_name_th: '',
                nick_name_en: '',
                email: '',
                phone: '',
                organization: '',
                occupation: '',
                year_grade: 0,
                faculty: '',
                department: '',
                event_id: [],
            };
        };

        onMounted(() => {
            fetchEvents();
        });

        return {
            events,
            form,
            onSubmit,
            onReset,
        };
    },
});
</script>

<style scoped>
.q-page {
    max-width: 700px;
    margin: 0 auto;
}
</style>