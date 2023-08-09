<style>
.scroll-short {
  height: 200px;
  /* 设置组件容器的固定高度 */
  overflow: auto;
  /* 设置溢出部分自动滚动 */
}
</style>

<template>
  <div>
    <a-typography-title>{{ key }}</a-typography-title>
    <a-row :gutter='12'>
      <a-col class="gutter-row" :span="12">
        <a-collapse>
          <a-collapse-panel header="History">
            <a-space direction="horizontal" align="baseline" v-for="h in data.profile.history">
              <a-button @click="copy(h)">
                <template #icon>
                  <CopyOutlined/>
                </template>
              </a-button>
              <p>{{ h }}</p>
              <!-- <a-textarea v-bind="h"> </a-textarea> -->


              <!-- <button v-on:click="setContent(item.id, h)">Set</button> -->

            </a-space>
          </a-collapse-panel>
        </a-collapse>

        <a-card title="Prompt">
          <a-button @click="() => { data.profile.messages.forEach((item) => item.enable = false) }">Disable
            All
          </a-button>
          <a-button @click="() => { data.profile.messages.forEach((item) => item.enable = true) }">Enable
            All
          </a-button>


          <div>
            <PromptInput :messages="data.profile.messages"
                         @order-up="id =>order(id,-1)"
                         @order-down="id =>order(id,1)"
                         @remove="id =>deletePrompt(id)"
                         @add="id =>addPrompt(id,'')"
            >

            </PromptInput>
          </div>

          <a-divider>
            <a-space>
              <a-button @click="() => data.profile.messages.push({})">
                <template #icon>
                  <PlusOutlined/>
                </template>
              </a-button>
            </a-space>

          </a-divider>

        </a-card>


      </a-col>


      <a-col class="gutter-row" :span="12">

        <a-collapse>

          <a-collapse-panel header="Snapshot">
            <div class="scroll-short">

              <div v-for="snapshot in data.profile.snapshots">
                <a-divider>
                  <a-button @click="useSnapshot(snapshot)">
                    Use Snapshot
                  </a-button>
                </a-divider>
                <PromptCard :messages="snapshot.prompt"></PromptCard>
                <a-textarea v-model:value="snapshot.response">

                </a-textarea>
              </div>
            </div>
          </a-collapse-panel>
        </a-collapse>


        <a-card title="Prompt Preview">
          <PromptCard :messages="data.profile.messages.filter((i) => i.enable)"></PromptCard>
        </a-card>

        <a-card title="Operation">
          <a-space direction="vertical">
            <a-space direction="horizontal">
              <a-button @click="chat">Chat</a-button>
              <a-button @click="snapshot">Snapshot</a-button>
              <a-button @click="reload">Reload</a-button>
              <a-button @click="gotoDebug">Goto Debug</a-button>
              <a-button @click="gotoIteration">Goto Iteration</a-button>
              <a-button @click="openNotification('test', 'info')">Notice</a-button>
            </a-space>

            <a-space direction="horizontal">
              <a-button @click="sendToPrompt">Send To Prompt</a-button>
              <a-button>Good</a-button>
              <a-button>Bad</a-button>
            </a-space>
          </a-space>
        </a-card>

        <a-card title="Corresponding Response">

          <a-textarea v-model:value="data.response" :auto-size="{ minRows: 20 }"
                      placeholder="textarea with clear icon" allow-clear/>
        </a-card>

      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import {useClipboard} from '@vueuse/core';
import {ref} from 'vue';

import {CopyOutlined, PlusOutlined} from '@ant-design/icons-vue';

import {useRoute, useRouter} from 'vue-router';
import {DefaultApiFactory} from '../../sdk/apis/default-api';

import {useSnapshotStore} from '@/stores/snapshot';

import type {NotificationPlacement} from "ant-design-vue";
import {notification} from 'ant-design-vue';
import type {Message, PromptItem, Snapshot} from "../../sdk";
import PromptCard from '../components/PromptCard.vue';
import PromptInput from "@/components/PromptInput.vue";
import {ApiFactory} from "@/scripts/api";

const [notification_api, contextHolder] = notification.useNotification();

// use
const store = useSnapshotStore()
const router = useRouter()
const {text, copy, copied, isSupported} = useClipboard({})
const api = ApiFactory()

// field

const key = ref<string>("")
const history = ref<any>([{
  messages: [
    {id: 1, role: "角色1", content: "内容1", enable: true, order: 0},
  ],
  response: ""
}])

const data = ref({
  response: <string>"",
  profile: {
    payload: "",
    "history": ["1"],
    "messages": [
      {id: 1, role: "角色1", content: "内容1", enable: true, order: 0, history: []},
      // 其他数据项
    ],
    "snapshots": [
      {
        "prompt": [
          {role: 'user', content: 'snapshot'}
        ],
        "response": ""
      }
    ]
  }
})

// created
const route = useRoute();
key.value = route.params.key.toString();
fetchProfile(key.value);

// methods
function sendToPrompt() {
  addPrompt(data.value.profile.messages[data.value.profile.messages.length - 1].id, data.value.response)
}

function deletePrompt(order: number) {
  let ms = data.value.profile.messages

  ms.splice(order, 1); // 删除指定索引的元素

  ms.forEach((elem, index) => elem.order = index)
}

function gotoIteration() {
  store.sendToIteration(data.value.profile.messages, key.value,)
  router.push('/view/iteration')
}

function gotoDebug() {
  store.sendToDebug(data.value.profile.messages, key.value,)
  router.push('/view/debug')
}

function useSnapshot(snapshot: Snapshot) {
  console.log(snapshot)
  let target = data.value.profile.messages
  let prompt = snapshot.prompt!!
  data.value.response = snapshot.response!!
  for (let i = 0; i < target.length; i++) {
    if (i >= prompt.length) {
      target[i].enable = false
    } else {
      target[i].enable = true
      target[i].role = prompt[i].role
      target[i].content = prompt[i].content
    }

  }
}

function snapshot() {

  let prompt: PromptItem[] = []
  data.value.profile.messages.forEach(
      (item: Message): any => {
        if (item.enable) {
          let res: PromptItem = {role: item.role, content: item.content}
          prompt.push(res)
        }

      }
  )
  let snapshot: Snapshot = {prompt: prompt, response: data.value.response}
  api.apiProfileKeySnapshotPost(snapshot, key.value,).then(() => {

  })
}

function addPrompt(id: number, content: string) {
  let index = data.value.profile.messages.findIndex((item) => item.id == id)
  let order = data.value.profile.messages[index].order
  let max_id = 0
  data.value.profile.messages.forEach((item) => {
    if (item.id > max_id) {
      max_id = item.id
    }
  })

  data.value.profile.messages.splice(
      index,
      0,
      {role: "user", id: max_id + 1, enable: true, content: content, order: order, history: []}
  )

  data.value.profile.messages.forEach((elem, index) => {
    elem.order = index;
    elem.id = index
  })

  console.log(data.value.profile.messages)
}

function order(id: number, delta: number) {
  let index = data.value.profile.messages.findIndex((m) => {
    return (m.id == id)
  })

  if (index < 0) {
    return
  }

  console.log(index)

  let temp = data.value.profile.messages[index]
  data.value.profile.messages[index] = data.value.profile.messages[index + delta]
  data.value.profile.messages[index + delta] = temp

  for (var i = 0; i < data.value.profile.messages.length; i++) {
    data.value.profile.messages[i].order = i
  }

  console.log(data.value.profile.messages)
}

function setContent(id: number, content: string) {
  data.value.profile.messages.forEach((m) => {
    if (m.id == id) {
      m.content = content
    }
  })
}

async function fetchProfile(key: string) {
  api.apiProfileKeyGet(key)
      .then(response => {
        data.value.profile = response.data;
      })
      .catch(error => {
        console.error(error);
        return null;
      });
}

function reload() {
  fetchProfile(key.value);
}


function openNotification(message: string, status: string) {
  let placement: NotificationPlacement = 'bottomRight'
  notification[status]({
    message: status,
    description: message,
    placement,
  });
}

function chat() {
  // console.log(data.value.payload)

  // let res = data.value.profile.messages.map(item => {
  //     let copied = {...item};
  //     copied.content = copied.content.replace('{{}}', data.value.payload)
  //     console.log(copied)
  //     return copied
  // })
  //
  // data.value.current = res

  let res = data.value.profile.messages


  console.log(res);
  api.apiChatKeyPost(res, key.value)
      .then(response => {
        console.log(response)

        data.value.response = response.data;
        console.log("result", response.data);
        console.log("data.value.response", data.value.response)
        history.value.push(
            {
              messages: data.value.profile.messages,
              response: response.data
            }
        )
      })
      .catch(error => {
        openNotification(error, 'error')
        console.error(error.toString());
        return;
      });

}
</script>
  