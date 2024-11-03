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
              <v-card-title>Upload Excel Dataset</v-card-title>
              <v-card-text>
                <v-file-input ref="file-input" @change="handleFileUpload" label="Dataset (XLSX)"></v-file-input>

                <div class="preview-container" v-if="fileInfo?.filename">
                  <v-card class="mt-5 pa-5 d-flex align-center text-blue-grey-darken-4" elevation="0" variant="outlined" color="blue-grey">
                    <v-icon class="pa-6">mdi-file-upload</v-icon>
                    <div class="div">
                      <h3>{{fileInfo?.filename}}</h3>
                      <p>{{ fileInfo?.size }}</p>
                    </div>
                  </v-card>

                  <v-btn class="mt-5" @click="uploadFile" color="blue-grey-darken-4" block>Upload</v-btn>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Uploaded Dataset (For Training)</v-card-title>
              <v-card-text>
                <v-card v-for="(file, i) in files" :key="i" class="mt-5 pa-5 d-flex align-center text-blue-grey-darken-4" elevation="0" variant="outlined" color="blue-grey">
                    <v-icon class="pa-6">mdi-file-upload</v-icon>
                    <div class="div">
                      <h3>{{ file }}</h3>
                      <p>XLSX Dataset File</p>
                    </div>
                    <v-btn @click="deleteFile(file)" class="ml-auto" color="red-darken-4" variant="fab" icon="mdi-delete"></v-btn>
                  </v-card>
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

const el = useTemplateRef('file-input')

const fileInfo = ref({
    filename: '',
    size: 0
  })

function handleFileUpload() {

  console.log('triggered')
  

  

  const hasFile = ref(false);

  console.log(el.value.files  )

  if (el.value.files && el.value.files[0]) {
    fileInfo.value = {
      filename: el.value.files[0].name,
      size: el.value.files[0].size
    }

    console.log(fileInfo.value)
  }

}

async function uploadFile() {

  const formData = new FormData();
  formData.append('file', el.value.files[0]);

  const response = await axios.post('http://localhost:5000/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': JSON.parse(userData.value).token
    }
  });

  if (response.error) {
    console.error('Error uploading file:', response.error);
    alert('Error uploading file');
    return;
  }

  console.log('Upload successful:', response.data);

  alert('Upload successful');

  window.location.reload();
}

const files = ref([]);

async function getFiles() {
const response = await axios.get('http://localhost:5000/get-files', {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': JSON.parse(userData.value).token
  }
});

if (response.error) {
  console.error('Error uploading file:', response.error);
  alert('Error uploading file');
  return;
}

console.log('Get files:', response.data);

files.value = response.data.files;
}

async function deleteFile(filename) {
const response = await axios.post('http://localhost:5000/delete-file', {
  filename: filename
} ,{
  headers: {
    'Content-Type': 'application/json',
    'Authorization': JSON.parse(userData.value).token
  }
});

if (response.error) {
  console.error('Error deleting file:', response.error);
  alert('Error deleting file');
  return;
}

console.log('Get files:', response.data);


getFiles();

alert('File deleted!');

}

onMounted(() => {
  console.log(userData.value)
  getFiles();
})
</script>

