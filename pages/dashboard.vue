<template>
  <v-app>
    <v-navigation-drawer color="#17509E">
      <v-list>
        <v-list-item class="py-5">
          <template v-slot:prepend>
            <v-avatar color="grey lighten-2" size="40">
              <v-img src="@/assets/img/avatar.png" alt="User Profile" />
            </v-avatar>
          </template>
          <v-list-item-content>
            <v-list-item-title>{{ JSON.parse(userData).user[1] }}</v-list-item-title>
            <v-list-item-subtitle>User Role</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item v-for="item in items" :key="item.title" :to="item.to" link>
          <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="white" dark>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn @click="logout" variant="text">Logout</v-btn>
    </v-app-bar>
    <v-main>
      <v-container class="mt-10" style="max-width: 1200px">
        <v-row>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Monthly Egg Production</v-card-title>
              <v-card-text>
                <!-- <v-chart
                  :option="option1"
                /> -->
                <v-img v-if="image1" :src="`http://localhost:5000/get-images/${image1}`"></v-img>
                <pre>{{ image1 }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Production Trend</v-card-title>
              <v-card-text>
                <!-- <v-chart
                  :option="option2"
                /> -->
                <v-img v-if="image2" :src="`http://localhost:5000/get-images/${image2}`"></v-img>
                <pre>{{ image2 }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useStorage } from '@vueuse/core'
import { ref } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import axios from 'axios'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const items = [
  { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
  { title: 'Upload Files', icon: 'mdi-file-upload', to: '/upload' },
  { title: 'Predictions', icon: 'mdi-lightbulb', to: '/predictions' },
  { title: 'Reports', icon: 'mdi-file-document', to: '/reports' },
  { title: 'Logout', icon: 'mdi-logout', to: '/logout' },
]

const userData = useStorage('userData', '');


let image1 = ref('');

let image2 = ref('');

async function generatePrediction() {
  
  let response;
  let response1 = await axios.get('http://localhost:5000/prediction', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': JSON.parse(userData.value).token
    }
  });
  let response2 = await axios.post('http://localhost:5000/generate-prediction', {
    months: 1
  }, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': JSON.parse(userData.value).token
    }
  });

if (response1.error) {
  console.error('Error fetching prediction:', response.error);
  // alert('Error fetching prediction');
  return;
}

if (response2.error) {
  console.error('Error fetching prediction:', response.error);
  // alert('Error fetching prediction');
  return;
}

image1.value = response1.data.filename;


image2.value = response2.data.filename;

console.log('Prediction files:', response.data);

data.value = response.data;

console.log(data.value)
}

onMounted(() => {
  console.log(userData.value)
  generatePrediction();
})
</script>

