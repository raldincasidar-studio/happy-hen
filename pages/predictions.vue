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
            <v-col cols="12" md="12">
              <v-card>
                <v-card-title>Monthly Egg Production</v-card-title>
                
                <v-card-text>
                    <p class="mb-4">Actual vs Predicted</p>
                    <v-row>
                        <v-col cols="12" md="4">
                            
                            <v-btn color="blue-grey-darken-4" class="my-4" elevation="0" @click="getFiles()">Show Accuracy</v-btn>
                        </v-col>
                        <v-col cols="12" md="8">
                            <v-img v-if="prediction?.filename" :src="`http://localhost:5000/get-images/${prediction?.filename}`"></v-img>
                            <v-table fixed-header>
                                <thead>
                                    <tr>
                                        <th class="text-left">Month</th>
                                        <th class="text-left" v-if="prediction?.actual">Actual</th>
                                        <th class="text-left">Predicted</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in prediction?.predicted_with_dates" :key="index">
                                        <td>{{ item.date }}</td>
                                        <td v-if="prediction?.actual">{{ prediction?.actual[index] }} eggs</td>
                                        <td>{{ item.predicted }} eggs</td>
                                    </tr>
                                </tbody>
                            </v-table>
                            <!-- <pre>{{ prediction }}</pre> -->
                        </v-col>
                    </v-row>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Generate Prediction</v-card-title>
                <v-card-text>
                  <p>Generate prediction based on data</p>
                  <v-select v-model="prediction_month" :items="months" label="Prediction month"></v-select>
                  <v-btn color="blue-grey-darken-4" class="my-4" @click="generatePrediction" elevation="0">Generate Predictions</v-btn>
                
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

  const months = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
  const prediction_month = ref(1)

  const items = [
    { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
    { title: 'Upload Files', icon: 'mdi-file-upload', to: '/upload' },
    { title: 'Predictions', icon: 'mdi-lightbulb', to: '/predictions' },
    { title: 'Reports', icon: 'mdi-file-document', to: '/reports' },
    { title: 'Logout', icon: 'mdi-logout', to: '/logout' },
  ]
  
  const userData = useStorage('userData', '');

  const prediction = ref({});
  

  async function generatePrediction() {
  
  const response = await axios.post('http://localhost:5000/generate-prediction', {
    months: prediction_month.value
  }, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': JSON.parse(userData.value).token
    }
  });
  
  if (response.error) {
    console.error('Error fetching prediction:', response.error);
    alert('Error fetching prediction');
    return;
  }
  
  console.log('Prediction files:', response.data);
  
  prediction.value = response.data;

  console.log(prediction.value)
  }




  async function getFiles() {
  const response = await axios.get('http://localhost:5000/prediction', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': JSON.parse(userData.value).token
    }
  });
  
  if (response.error) {
    console.error('Error fetching prediction:', response.error);
    alert('Error fetching prediction');
    return;
  }
  
  console.log('Prediction files:', response.data);
  
  prediction.value = response.data;

  console.log(prediction.value)
  }
  
  
  onMounted(() => {
    console.log(userData.value)
    getFiles();
  })
  </script>
  
  