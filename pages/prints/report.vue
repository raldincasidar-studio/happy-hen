<template>
<div class="paper">
    <div style="text-align: center;">
        <h1 style="text-align: center; font-size: 25px">Happy Hen Reports</h1>
        <h1 style="text-align: center; font-size: 20px">{{ useRoute().query.type }}</h1>
        <h1 style="text-align: center; font-size: 20px">{{ new Date().toLocaleString('default', { month: 'long', day: 'numeric', year: 'numeric' }) }}</h1>
        <div class="divider" style="border-bottom: 1px solid gray; margin: 20px 0"></div>
    </div>
    <img style="max-width: 100%" v-if="data?.filename" :src="`http://localhost:5000/get-images/${data?.filename}`">
    <h3 style="margin-top: 20px;">Insights</h3>
    <p style="font-size: 15px; margin: 10px 0">Based on the current trend, the predicted egg production for the future 3 months will be:</p>
    <table style="width: 100%">
        <tr>
            <th>Month</th>
            <th>{{ data.actual ? 'Actual' : 'Predicted' }}</th>
        </tr>
        <tr v-for="(item, index) in data?.predicted_with_dates" :key="index">
            <td>{{ item.date }}</td>
            <td>{{ data?.actual ? data.actual[index] : item.predicted }} eggs</td>
        </tr>
    </table>
    <h3 style="margin-top: 50px;">What to do?</h3>
    <p style="font-size: 15px; margin: 10px 0">To boost egg production, farmers can start by focusing on the nutrition their hens receive. A balanced diet packed with protein, calcium, vitamins, and minerals is essential, as these nutrients directly impact the quality and number of eggs laid. Consider adding a little extra calcium for stronger eggshells and vitamin D to help hens absorb nutrients better. Keeping a consistent feeding schedule is also key—irregular feeding can cause stress, which affects laying frequency.</p>

    <p style="font-size: 15px; margin: 10px 0">The environment in which hens live is just as important. Every hen needs enough space to feel comfortable, as overcrowding can lead to stress and aggression, which reduces egg production. Maintaining a coop temperature between 55–75°F (13–24°C) with good ventilation helps keep moisture levels down and the air fresh, creating a more productive and healthy space for the flock.</p>

    <p style="font-size: 15px; margin: 10px 0">Lighting also plays a big role. Hens generally need 14-16 hours of light each day to keep laying at a high rate. During seasons when daylight is shorter, adding some artificial light can help them stay on schedule. Use warm, gentle lights to keep them relaxed and laying consistently.</p>

    <p style="font-size: 15px; margin: 10px 0">Keeping hens healthy is vital to sustaining egg production. Regular health checkups and vaccines protect against common diseases like avian flu and Newcastle disease, which can devastate a flock. Watch for mites and lice as well, as these parasites can impact their health and reduce egg-laying. Finally, during molting periods, when hens naturally slow down in production, consider adjusting their diet and care to support them through this phase. With a little extra attention, they’ll bounce back to their regular laying rates in no time.</p>
    <!-- <pre>{{ data }}</pre> -->
</div>
</template>

<style scoped>
.paper {
    max-width: 700px;
    margin: auto;
    padding: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 16px;
    text-align: left;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
}

th {
    background-color: #f2f2f2;
    color: black;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* tr:hover {
    background-color: #f1f1f1;
} */
</style>

<script setup>
  import { useStorage } from '@vueuse/core'
    import axios from 'axios'
const data = ref({})

const userData = useStorage('userData', '');

async function generatePrediction() {
  
    let response;
  if (useRoute().query.type === 'Descriptive Report') {
    response = await axios.get('http://localhost:5000/prediction', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': JSON.parse(userData.value).token
      }
    });
  } else {
    response = await axios.post('http://localhost:5000/generate-prediction', {
      months: 3
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': JSON.parse(userData.value).token
      }
    });
  }
  
  if (response.error) {
    console.error('Error fetching prediction:', response.error);
    alert('Error fetching prediction');
    return;
  }
  
  console.log('Prediction files:', response.data);
  
  data.value = response.data;

  console.log(data.value)

  setTimeout(() => {
    window.print()
    window.close()
  }, 1000);
  }

onMounted(() => {
  console.log(userData.value)
  generatePrediction();
})

</script>