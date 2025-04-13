<template>
    <div class="container mt-5">
      <h2 class="text-center mb-4">Movies</h2>
      <div class="row justify-content-center">
        <div class="col-md-4 mb-4" v-for="movie in movies" :key="movie.id">
          <div class="card h-100">
            <img :src="movie.poster" class="card-img-top" alt="Movie Poster" />
            <div class="card-body">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text">{{ movie.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let movies = ref([]);
  
  const fetchMovies = () => {
    fetch("/api/v1/movies")
      .then((response) => response.json())
      .then((data) => {
        movies.value = data.movies;
      })
      .catch((error) => {
        console.error("Failed to fetch movies:", error);
      });
  };
  
  onMounted(() => {
    fetchMovies();
  });
  </script>
  
  <style scoped>
  .card-img-top {
    max-height: 300px;
    object-fit: cover;
  }
  </style>
  