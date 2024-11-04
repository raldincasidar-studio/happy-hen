<template>
    <h3>Logging out ...</h3>
</template>

<script setup>

import { useStorage } from '@vueuse/core'

const userData = useStorage('userData', '')

userData.value = {};

useRouter().replace('/')

</script>