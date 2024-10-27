<template>
    <div class="login-page">
        <div class="card-container">
            <v-card width="400">
                <v-card-title class="text-center my-7">
                    <v-img src="@/assets/img/logo.svg" style="max-width: 100px; margin: 20px auto"></v-img>
                    <h2>Happy Hen</h2>
                    <p class="text-grey my-1">Administrator Login</p>
                </v-card-title>
                <v-card-text>
                    <v-form>
                        <v-text-field
                            v-model="username"
                            label="Username"
                            type="text"
                            variant="outlined"
                        ></v-text-field>
                        <v-text-field
                            v-model="password"
                            label="Password"
                            type="password"
                            variant="outlined"
                        ></v-text-field>
                        <div class="d-flex justify-space-between mt-4">
                            <v-btn color="primary" variant="elevated" block size="large" @click="login">
                                Login
                            </v-btn>
                        </div>
                    </v-form>
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios'
import { useStorage } from '@vueuse/core'


const username = ref('')
const password = ref('') 
const login = async () => {
    try {
        const response = await axios.post('http://localhost:5000/login', {
            username: username.value,
            password: password.value
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('Login successful:', response.data);


        const userData = useStorage('userData', '')

        userData.value = JSON.stringify(response.data);
        
        alert('Login successful');

        const router = useRouter()
        router.push('/dashboard')
    } catch (error) {
        console.error('Error logging in:', error.response ? error.response.data : error.message);
        alert('Login failed', error.response ? error.response.data : error.message);
    }
}
</script>

<style lang="scss" scoped>
    .login-page {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        background-color: #17509E;

        .card-container {
            width: 100%;
            max-width: 400px;
        }
    }
</style>