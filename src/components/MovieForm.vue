<template>
    <div>
      <form @submit.prevent="saveMovie" id="movieForm">
        <div class="form-group mb-3">
          <label for="title" class="form-label">Movie Title</label>
          <input type="text" name="title" class="form-control" v-model="title" required />
        </div>
        <div class="form-group mb-3">
          <label for="description" class="form-label">Movie Description</label>
          <textarea name="description" class="form-control" v-model="description" required></textarea>
        </div>
        <div class="form-group mb-3">
          <label for="poster" class="form-label">Movie Poster</label>
          <input type="file" name="poster" class="form-control" ref="poster" required />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const title = ref('');
const description = ref('');
const csrf_token = ref('');
const poster = ref(null); 
const BASE_URL = "http://localhost:8080"; 

// Fetch the CSRF token from Flask
const getCsrfToken = async () => {
  try {
    const response = await fetch(`${BASE_URL}/api/v1/csrf-token`, {
      credentials: 'include'  
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch CSRF token: ${response.status}`);
    }
    const data = await response.json();
    csrf_token.value = data.csrf_token;
    console.log('Fetched CSRF Token:', data.csrf_token);
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
  }
};

// Call getCsrfToken when the component is mounted
onMounted(() => {
  getCsrfToken();
});

const saveMovie = () => {
  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);

  // Add CSRF token to the form data
  form_data.append('csrf_token', csrf_token.value);

  fetch(`${BASE_URL}/api/v1/movies`, {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value 
    }
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    console.log('Movie saved successfully:', data);
  })
  .catch((error) => {
    console.error('Error saving movie:', error);
  });
};
</script>
