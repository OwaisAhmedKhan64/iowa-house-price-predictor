<template>
    <div id="app" class="container">
        <header class="header">
            <h1>Melbourne House Price Predictor</h1>
            <p>Enter the details below to estimate the property value.</p>
        </header>
        
        <div class="content-row">
            <div class="result-section">
                <div v-if="prediction !== null" class="result-card success">
                    <h3>Estimated Value</h3>
                    <p class="price">${{ prediction.toLocaleString() }}</p>
                </div>

                <div v-else class="result-card placeholder">
                    <h3>Ready to Predict</h3>
                    <p>Fill out the form on the right and click predict to see the result here.</p>
                </div>

                <div v-if="error" class="error-message">
                    {{ error }}
                </div>
            </div>

            <div class="form-section">
                <div class="card">
                    <div class="form-group">
                        <label>Number of Rooms</label>
                        <input v-model="formData.Rooms" type="number" min="1" step="1">
                    </div>

                    <div class="form-group">
                        <label>Number of Bathrooms</label>
                        <input v-model="formData.Bathroom" type="number" min="1" step="1">
                    </div>

                    <div class="form-group">
                        <label>Distance from CBD (km)</label>
                        <input v-model="formData.Distance" type="number" min="1" step="1">
                    </div>

                    <div class="form-group">
                        <label>Landsize (sqm)</label>
                        <input v-model="formData.Landsize" type="number" min="1" step="1">
                    </div>

                    <div class="form-group">
                        <label>Property Type</label>
                        <select v-model="formData.Type">
                            <option value="h">House / Cottage / Villa</option>
                            <option value="u">Unit / Duplex</option>
                            <option value="t">Townhouse</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Region</label>
                        <select v-model="formData.Regionname">
                            <option v-for="region in regions" :key="region" :value="region">
                                {{ region }}
                            </option>
                        </select>
                    </div>

                    <button @click="predictPrice" :disabled="loading" class="predict-btn">
                        {{ loading ? 'Calculating' : 'Predict Price' }}
                    </button>

                </div>

            </div>
            
        </div>

    </div>
    
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

// 1. DATA STATE
const formData = reactive({
    Rooms: 3,
    Bathroom: 1,
    Distance: 10,
    Landsize: 400,
    Type: 'h',
    Regionname: 'Southern Metropolitan',
})

const prediction = ref(null)
const loading = ref(false)
const error = ref(null)

const regions = [
    'Northern Metropolitan',
    'Western Metropolitan',
    'Southern Metropolitan',
    'Eastern Metropolitan',
    'South-Eastern Metropolitan',
    'Eastern Victoria',
    'Northern Victoria',
    'Western Victoria'
]

const predictPrice = async () =>
{
    loading.value = true
    error.value = null
    prediction.value = null
    
    try
    {
        const response = await axios.post ('http://127.0.0.1:8000/api/predict/', formData)
        prediction.value = response.data.predicted_price
    }
    catch (err)
    {
        error.value = "Could not connect to backend."
        console.error(err)
    }
    finally
    {
        loading.value = false
    }
}

</script>

<style scoped>
/* GENERAL LAYOUT */
.container {
  max-width: 1000px; /* Made wider to fit two columns */
  margin: 40px auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 0 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

/* FLEXBOX LAYOUT (The Magic Part) */
.content-row {
  display: flex;
  flex-direction: row; /* Horizontal alignment */
  gap: 40px;           /* Space between Result and Form */
  align-items: flex-start; /* Align to top */
}

.result-section {
  flex: 1; /* Takes up 1 part of space */
  position: sticky;
  top: 20px; /* Keeps result in view if scrolling */
}

.form-section {
  flex: 1; /* Takes up 1 part of space */
}

/* CARDS & FORMS */
.card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.result-card {
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}

.success {
  background: #e8f5e9;
  border: 2px solid #42b983;
  color: #2c3e50;
}

.placeholder {
  background: #f1f3f5;
  border: 2px dashed #ced4da;
  color: #6c757d;
}

.price {
  font-size: 42px;
  font-weight: 800;
  color: #42b983;
  margin: 10px 0;
}

/* FORM ELEMENTS */
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #34495e;
}

input, select {
  width: 100%;
  padding: 12px;
  border: 1px solid #dfe6e9;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box; /* Important for width */
}

input:focus, select:focus {
  outline: none;
  border-color: #42b983;
}

/* BUTTONS */
.predict-btn {
  width: 100%;
  padding: 15px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.predict-btn:hover {
  background-color: #34495e;
}

.predict-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 6px;
  margin-top: 20px;
  text-align: center;
}

/* MOBILE RESPONSIVE: Stack them vertically on small screens */
@media (max-width: 768px) {
  .content-row {
    flex-direction: column-reverse; /* Form first, Result bottom */
  }
}
</style>