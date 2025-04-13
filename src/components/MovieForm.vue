<template>
  <div class="container py-4" style="max-width: 600px; margin: 0 auto;">
    <!-- Success message -->
    <p v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </p>

    <!-- Error messages -->
    <div v-if="errorMessages.length" class="alert alert-danger">
      <ul class="mb-0">
        <li v-for="(msg, idx) in errorMessages" :key="idx">{{ msg }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie" class="border p-4 rounded shadow-sm bg-white">
      <div class="form-group mb-3">
        <label for="title" class="form-label fw-bold">Movie Title</label>
        <input type="text" name="title" v-model="title" class="form-control" required />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label fw-bold">Movie Description</label>
        <textarea name="description" v-model="description" class="form-control" rows="4" required></textarea>
      </div>

      <div class="form-group mb-4">
        <label for="poster" class="form-label fw-bold">Poster</label>
        <input type="file" name="poster" @change="handleFileChange" class="form-control" accept="image/*" required />
      </div>

      <div class="d-grid">
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

// Fetch CSRF token when the component is mounted
function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data); // Check if the token is correctly fetched
            csrf_token.value = data.csrf_token;
        });
}

onMounted(() => {
    getCsrfToken();
});

// Define form data properties
const title = ref('');
const description = ref('');
const poster = ref(null);

// Feedback message states
const successMessage = ref('');
const errorMessages = ref([]);

// Method to handle file input change
const handleFileChange = (event) => {
  // Get the selected file from the input
  poster.value = event.target.files[0];
  console.log(poster.value);
};

// Method to save movie data
function saveMovie() {
  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);

  if (!form_data.has("poster") && poster.value) {
    form_data.append("poster", poster.value);
  }

  form_data.append("csrf_token", csrf_token.value);

  for (let [key, value] of form_data.entries()) {
    console.log(`${key}:`, value);
  }

  fetch("/api/v1/movies", {
    method: 'POST',
    body: form_data
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          // Reset success message
          successMessage.value = '';
          // Set error messages
          errorMessages.value = data.error ? [data.error] : data.errors || ["An error occurred."];
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data && data.message) {
        // Set success message
        successMessage.value = data.message;
        errorMessages.value = [];

        // Clear form fields
        title.value = '';
        description.value = '';
        poster.value = null;

        
        document.querySelector('input[name="poster"]').value = '';
      }
    })
    .catch((error) => {
      console.log(error);
      successMessage.value = '';
      errorMessages.value = ["Something went wrong. Try again later."];
    });
}
</script>
