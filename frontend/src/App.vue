<template>
    <div id="app" class="container">
        <h1>Melbourne House Price Predictor</h1>
        <p>Enter the details below to estimate the property value.</p>

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

            <button @click="predictPrice" :disabled="loading">
                {{ loading ? 'Calculating' : 'Predict Price' }}
            </button>

        </div>
        
        <div v-if="prediction !== null" class="result-card">
            <h2>Estimated Price</h2>
            <p class="price">${{ prediction.toLocaleString() }}</p>
        </div>

        <div v-if="error" class="error-message">
            {{ error }}
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
.container {
  max-width: 550px;
  margin: 50px auto;
  font-family: sans-serif;
  text-align: center;
}
.card {
  background: #f9f9f9;
  padding: 30px;
  border-radius: 8px;
  text-align: left;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:disabled {
  background-color: #a0d9bc;
}
.result-card {
  margin-top: 20px;
  padding: 20px;
  border: 2px solid #42b983;
  border-radius: 8px;
}
.price {
  font-size: 32px;
  font-weight: bold;
  color: #42b983;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>