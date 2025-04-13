<template>
  <div>
    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" v-model="title" class="form-control" required />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Movie Description</label>
        <textarea name="description" v-model="description" class="form-control" required></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input type="file" name="poster" @change="handleFileChange" class="form-control" accept="image/*" required />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

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
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });
}


</script>
