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
    console.error('Error fetching audience by event', error);
    throw error;
  }
};

//Get  audience by event ID
export const getAudiences = async (eventId: number) => {
  try {
    const response = await axios.get(`${API_URL}/audience/event/${eventId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching audience', error);
    throw error;
  }
};

//Post Register Audience
export const registerAudience = async (form: any) => {
  try {
    const response = await axios.post(`${API_URL}/audience`, form); // ส่งข้อมูลฟอร์มใน body
    return response;
  } catch (error) {
    console.error('Error registering audience', error);
    throw error;
  }
};

//Post Check-in
export const postCheckin = async (form: any) => {
  console.log(form, 'postCheckin');
  try {
    const response = await axios.post(`${API_URL}/checkin`, form); // ส่งข้อมูลฟอร์มใน body
    return response.data;
  } catch (error) {
    console.error('Error registering audience', error);
    throw error;
  }
};
