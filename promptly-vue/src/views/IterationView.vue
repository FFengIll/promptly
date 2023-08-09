<script setup lang="ts">
import {ref} from "vue";
import type {Iteration, Message} from "../../sdk";
import PromptInput from "@/components/PromptInput.vue";
import {ApiFactory} from "@/scripts/api";
import {useSnapshotStore} from "@/stores/snapshot";
import router from "@/router";

const api = ApiFactory()
const store = useSnapshotStore()

const autoSave = ref<boolean>(true)
const key = ref<string>(store.iterationSource.toString())
const data = ref<Iteration[]>(
    [
      {
        response: "Hi!",
        messages: <Message[]>[
          {
            role: 'user',
            content: "hello",
            enable: true
          }
        ]
      }
    ]
)

getIteration(key.value)

function getIteration(name: string) {
  let source = {messages: store.iteration}
  api.apiIterationGet(name).then(
      response => {
        key.value = response.data.name
        data.value = response.data.iters.filter(item => item.messages.length > 0)
        console.log(data.value)

      }
  ).catch(error => {
    console.log(error)
  })

  if (source.messages.length > 0) {
    data.value.push(source)
  }

}

function nextIteration(ref) {
  let another = JSON.parse(JSON.stringify(ref))
  another.response = ""

  data.value.unshift(another)
}


async function doChat(it: Iteration) {
  if (autoSave) {
    await saveIteration(key.value, data.value)
  }

  console.log(it.messages)

  let ms = it.messages?.filter((item) => item.enable)
  console.log("will chat with messages", ms)
  await api.apiChatPost(ms).then(
      (response) => {
        it.response = response.data
      }
  )
}

function gotoDebug(it: Iteration) {
  store.sendToDebug(it.messages, '')
  router.push('/view/debug')
}

async function saveIteration(key, data: Iteration[]) {
  await api.apiIterationPost(data, key).then(
      response => {
        console.log("success")
      }
  )
}

function dropIteration(index) {
  console.log(index)
  data.value.splice(index, 1)
}

</script>

<template>
  <a-row :gutter="[16,16]">
    <a-col :span="24" class="gutter-row">
      <a-space direction="horizontal">
        <a-input-group compact>
          <a-input v-model:value="key" style="width: 100px"/>
          <a-button type="primary" @click="getIteration(key)">Get</a-button>
          <a-button type="primary" @click="saveIteration(key, data)">Save</a-button>
        </a-input-group>
        <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
        <a-button @click="nextIteration( data[0])">Next</a-button>
      </a-space>
    </a-col>
  </a-row>
  <a-row :gutter="[16,16]">
    <a-col :span="8" v-for="(prompt,index) in data" align="center" :key="index">
      <a-card>
        <!--        response-->
        <a-textarea v-model:value="prompt.response"
                    :auto-size="{ minRows: 5 ,maxRows:10 }"
        >

        </a-textarea>

        <!--        button-->
        <a-button @click="doChat(prompt)">Request</a-button>
        <a-button @click="gotoDebug(prompt)">Go To Debug</a-button>
        <a-button @click="nextIteration(prompt)">Next</a-button>
        <a-button @click="dropIteration(index)">Drop</a-button>


        <!--        prompt-->
        <PromptInput :messages="prompt.messages" mode="simple">

        </PromptInput>

      </a-card>


    </a-col>
  </a-row>
</template>

<style>

</style>
