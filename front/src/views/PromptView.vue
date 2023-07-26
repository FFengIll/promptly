<template>
  <div>
    <a-row :gutter='12'>
      <a-col class="gutter-row" :span="14">
        <a-card title="Prompt">
          <div v-for="item in profile.messages" :key="item.id" class="card">
            <!-- <template #extra><a href="#">more</a></template> -->

            <a-row :gutter="12" align="middle">
              <a-col :span="4">
                <a-space direction="vertical">
                  <!-- role select -->
                  <a-select ref="select" v-model:value="item.role" style="width: 120px">
                    <a-select-option value="user">User</a-select-option>
                    <a-select-option value="system">System</a-select-option>
                    <a-select-option value="assistant">Assistant</a-select-option>
                  </a-select>

                  <!-- enable toggle -->
                  <a-space direction="horizontal">
                    Enable&nbsp;
                    <a-switch v-model:checked="item.enable"></a-switch>
                  </a-space>

                </a-space>
              </a-col>
              <a-col :span="16">
                <!-- content edit -->
                <a-textarea v-model:value="item.content" placeholder="textarea with clear icon" allow-clear
                            :auto-size="{ minRows: 3, maxRows: 5 }"/>

              </a-col>
              <a-col :span="2">
                <a-space direction="vertical">
                  <!-- up down the order -->
                  <a-button type="primary" shape="round" @click="order(item.id, -1)">
                    <template #icon>
                      <UpOutlined/>
                    </template>
                  </a-button>
                  <a-button type="primary" shape="round" @click="order(item.id, 1)">
                    <template #icon>
                      <DownOutlined/>
                    </template>
                  </a-button>
                </a-space>
              </a-col>
              <a-col :span="2">

                <a-button @click="addContent(item.id,item.order)">
                  <template #icon>
                    <PlusOutlined/>
                  </template>
                </a-button>
              </a-col>
            </a-row>

            <a-collapse>
              <a-collapse-panel>
                <div v-for="h in item.history">
                  <a-space direction="horizontal">

                    <p>{{ h }}</p>
                    <!-- <a-textarea v-bind="h"> </a-textarea> -->

                    <!-- <button v-on:click="copy(h)">复制到剪贴板</button> -->

                    <button v-on:click="setContent(item.id, h)">Set</button>

                  </a-space>
                </div>
              </a-collapse-panel>
            </a-collapse>
          </div>
        </a-card>
      </a-col>
      <a-col class="gutter-row" :span="10">
        <a-card title="Operation">
          <a-button @click="reload">reload</a-button>
          <a-button @click="chat">Chat</a-button>
          <a-button @click="goToDebug">Go To Debug</a-button>
          <a-button>Good</a-button>
          <a-button>Bad</a-button>
        </a-card>

        <a-card title="Prompt Result">
          <div v-for="item in profile.messages">
            <a-list-item v-if="item.enable">
              <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
              <span>{{ item.content }}</span>
            </a-list-item>
          </div>
          <a-textarea v-model:value="response" :auto-size="{ minRows: 20 }" placeholder="textarea with clear icon"
                      allow-clear/>
        </a-card>

      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts">
import useClipboard from 'vue-clipboard3';

import {DownOutlined, PlusOutlined, UpOutlined} from '@ant-design/icons-vue';

import {useRoute} from 'vue-router';
import {DefaultApiFactory} from '../../sdk/apis/default-api';

import {useSnapshotStore} from '@/stores/snapshot';
import {mapActions} from 'pinia';

const api = DefaultApiFactory(undefined, "http://localhost:8000")
const {toClipboard} = useClipboard()

export default {
  // props: ['key'],
  data() {
    return {
      modal: false,
      key: "",
      history: [{
        messages: [],
        response: ""
      }],
      response: "",
      profile: {
        "messages": [
          {id: 1, role: "角色1", content: "内容1", enable: true, order: 0},
          {id: 2, role: "角色2", content: "内容2", enable: true, order: 1},
          {id: 3, role: "角色3", content: "内容3", enable: false, order: 2},
          // 其他数据项
        ]
      }
    };
  },
  mounted() {
  },
  created() {
    const route = useRoute();
    this.key = route.params.key.toString();
    this.fetchProfile(this.key);

    const store = useSnapshotStore()
  },
  components: {
    UpOutlined,
    DownOutlined,
    PlusOutlined,
  },
  computed: {
    api: () => api,
  },
  methods: {
    ...mapActions(useSnapshotStore, ['sendToDebug']),

    goToDebug() {
      this.sendToDebug(this.profile.messages)
      this.$router.push('/view/debug')
    },
    addContent(id: number, order: number) {
      var index = this.profile.messages.findIndex((item) => item.id == id)
      var order = this.profile.messages[index].order
      var max_id = 0
      this.profile.messages.forEach((item) => {
        if (item.id > max_id) {
          max_id = item.id
        }
      })

      this.profile.messages.splice(
          index + 1,
          0,
          {role: "user", id: max_id + 1, enable: true, content: "", order: order}
      )

      var cur = 0
      this.profile.messages.forEach((item) => {
        item.order = cur;
        cur++;
      })

      console.log(this.profile.messages)
    },
    order(id: number, delta: number) {
      let index = this.profile.messages.findIndex((m) => {
        return (m.id == id)
      })

      if (index < 0) {
        return
      }

      console.log(index)

      let temp = this.profile.messages[index]
      this.profile.messages[index] = this.profile.messages[index + delta]
      this.profile.messages[index + delta] = temp

      for (var i = 0; i < this.profile.messages.length; i++) {
        this.profile.messages[i].order = i
      }

      console.log(this.profile.messages)
    },
    setContent(id: number, content: string) {
      this.profile.messages.forEach((m) => {
        if (m.id == id) {
          m.content = content
        }
      })
    },
    async copy(content: string) {
      await toClipboard(content)
    },
    handleOk(e: MouseEvent) {
      console.log(e);
      this.modal = false;
    },
    async fetchProfile(key: string) {
      this.api.loadProfileProfileKeyGet(key)
          .then(response => {
            this.profile = response.data.profile;
          })
          .catch(error => {
            console.error(error);
            return null;
          });
    },
    reload() {
      this.fetchProfile(this.key);
    },
    chat() {
      var res = this.profile.messages;
      console.log(res);
      this.api.chatChatKeyPost(res, this.key)
          .then(response => {
            console.log(response.data);
            this.response = response.data;

            this.history.push(
                {
                  messages: this.profile.messages,
                  response: response.data
                }
            )
          })
          .catch(error => {
            console.error(error);
            return;
          });

    },
  },
};
</script>
  