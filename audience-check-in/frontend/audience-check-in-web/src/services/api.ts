import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Adjust this URL if needed

// Get events
export const getEvents = async () => {
    try {
        const response = await axios.get(`${API_URL}/events/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching events', error);
        throw error;
    }
};

// Get check-ins by event ID
export const getCheckins = async (eventId: number) => {
    try {
        const response = await axios.get(`${API_URL}/checkin/event/${eventId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching check-ins', error);
        throw error;
    }
};

export const getAudienceByEvent = async (eventId: number) => {
    try {
        const response = await axios.get(`${API_URL}/audience/event/${eventId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching audience by event", error);
        throw error;
    }
};
