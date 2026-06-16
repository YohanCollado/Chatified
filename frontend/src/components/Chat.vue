<template>
  <main class="chat-page">
    <section class="chat-shell">
      <header class="chat-header">
        <div>
          <p class="chat-label">Chatified</p>
          <h1>Start chatting</h1>
        </div>

        <div v-if="shareUrl" class="share-panel">
          <input
            class="share-input"
            type="text"
            :value="shareUrl"
            readonly
            aria-label="Shareable chat URL"
            @focus="$event.target.select()"
          />
          <button class="btn secondary-btn" type="button" @click="copyShareUrl">
            {{ copied ? 'Copied' : 'Copy' }}
          </button>
        </div>
      </header>

      <div class="chat-body">
        <div v-if="loading" class="empty-state">
          Loading chat...
        </div>

        <div v-else-if="messages.length === 0" class="empty-state">
          No messages yet.
        </div>

        <div
          v-else
          v-for="(message, index) in messages"
          :key="index"
          class="message-row"
          :class="{ 'message-row-user': isCurrentUser(message) }"
        >
          <article class="message-bubble">
            <strong>{{ displayName(message) }}</strong>
            <p>{{ message.message }}</p>
          </article>
        </div>
      </div>

      <form class="chat-composer" @submit.prevent="sendMessage">
        <input
          v-model.trim="newMessage"
          type="text"
          placeholder="Type a message"
          :disabled="!currentChatUri || sending"
        />
        <button
          class="btn primary-btn"
          type="submit"
          :disabled="!newMessage || !currentChatUri || sending"
        >
          Send
        </button>
      </form>

      <p v-if="errorMessage" class="chat-error">{{ errorMessage }}</p>
    </section>
  </main>
</template>

<script>
const API_BASE_URL = 'http://localhost:8000/api'

function requestJson (method, url, data, authToken) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()

    request.open(method, url)
    request.setRequestHeader('Content-Type', 'application/json')

    if (authToken) {
      request.setRequestHeader('Authorization', `Token ${authToken}`)
    }

    request.onload = () => {
      let response = {}

      try {
        response = request.responseText ? JSON.parse(request.responseText) : {}
      } catch (error) {
        response = { message: request.responseText || 'The server returned an invalid response.' }
      }

      if (request.status >= 200 && request.status < 300) {
        resolve(response)
      } else {
        reject(new Error(response.detail || response.message || JSON.stringify(response)))
      }
    }

    request.onerror = () => reject(new Error('Unable to reach the server.'))
    request.send(data ? JSON.stringify(data) : null)
  })
}

function getStoredValue (key) {
  if (!window.sessionStorage) {
    return null
  }

  return window.sessionStorage.getItem(key)
}

export default {
  data () {
    return {
      copied: false,
      currentChatUri: '',
      errorMessage: '',
      loading: true,
      messages: [],
      newMessage: '',
      sending: false,
      username: ''
    }
  },

  computed: {
    shareUrl () {
      if (!this.currentChatUri) {
        return ''
      }

      return `${window.location.origin}/#/chats/${this.currentChatUri}`
    }
  },

  created () {
    this.username = getStoredValue('username') || ''
    this.currentChatUri = this.$route.params.uri || ''

    if (this.currentChatUri) {
      this.loadMessages()
    } else {
      this.startChatSession()
    }
  },

  watch: {
    '$route.params.uri' (uri) {
      this.currentChatUri = uri || ''
      this.messages = []

      if (this.currentChatUri) {
        this.loadMessages()
      }
    }
  },

  methods: {
    authToken () {
      const authToken = getStoredValue('authToken')

      if (!authToken) {
        this.errorMessage = 'Please sign in before chatting.'
        this.$router.push('/auth')
      }

      return authToken
    },

    copyShareUrl () {
      if (!this.shareUrl) {
        return
      }

      if (navigator.clipboard) {
        navigator.clipboard.writeText(this.shareUrl)
      }

      this.copied = true
      window.setTimeout(() => {
        this.copied = false
      }, 1500)
    },

    displayName (message) {
      return message.user && message.user.username ? message.user.username : 'Guest'
    },

    isCurrentUser (message) {
      return message.user && message.user.username === this.username
    },

    loadMessages () {
      const authToken = this.authToken()

      if (!authToken) {
        return
      }

      this.loading = true
      this.errorMessage = ''

      requestJson('GET', `${API_BASE_URL}/chats/${this.currentChatUri}/messages/`, null, authToken)
        .then((data) => {
          this.messages = data.messages || []
        })
        .catch((error) => {
          this.errorMessage = error.message
        })
        .then(() => {
          this.loading = false
        })
    },

    sendMessage () {
      const authToken = this.authToken()

      if (!authToken || !this.newMessage) {
        return
      }

      const message = this.newMessage
      this.sending = true
      this.errorMessage = ''

      requestJson(
        'POST',
        `${API_BASE_URL}/chats/${this.currentChatUri}/messages/`,
        { message },
        authToken
      )
        .then((data) => {
          this.messages.push({
            message: data.messages || message,
            user: data.user || { username: this.username }
          })
          this.newMessage = ''
        })
        .catch((error) => {
          this.errorMessage = error.message
        })
        .then(() => {
          this.sending = false
        })
    },

    startChatSession () {
      const authToken = this.authToken()

      if (!authToken) {
        return
      }

      this.loading = true
      this.errorMessage = ''

      requestJson('POST', `${API_BASE_URL}/chats/`, {}, authToken)
        .then((data) => {
          this.currentChatUri = data.uri
          this.$router.replace(`/chats/${data.uri}`)
        })
        .catch((error) => {
          this.errorMessage = error.message
        })
        .then(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.chat-page {
  min-height: calc(100vh - 60px);
  padding: 32px 16px;
  background: #f5f7fb;
}

.chat-shell {
  display: flex;
  flex-direction: column;
  width: min(860px, 100%);
  min-height: 620px;
  margin: 0 auto;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #dde3ed;
  border-radius: 8px;
  box-shadow: 0 16px 40px rgba(33, 45, 70, 0.08);
  text-align: left;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 20px;
  border-bottom: 1px solid #e6ebf2;
}

.chat-label {
  margin: 0 0 4px;
  color: #667085;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

.chat-header h1 {
  margin: 0;
  color: #172033;
  font-size: 24px;
  font-weight: 700;
}

.share-panel {
  display: flex;
  gap: 8px;
  width: min(420px, 100%);
}

.share-input,
.chat-composer input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  color: #172033;
  background: #ffffff;
  border: 1px solid #ccd5e1;
  border-radius: 6px;
  font-size: 14px;
}

.share-input {
  background: #f8fafc;
}

.chat-body {
  flex: 1;
  min-height: 400px;
  padding: 20px;
  overflow-y: auto;
  background: #fbfcfe;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 320px;
  color: #697386;
  font-size: 15px;
}

.message-row {
  display: flex;
  margin-bottom: 12px;
}

.message-row-user {
  justify-content: flex-end;
}

.message-bubble {
  max-width: min(74%, 560px);
  padding: 10px 12px;
  color: #172033;
  background: #eef2f7;
  border-radius: 8px;
}

.message-row-user .message-bubble {
  color: #ffffff;
  background: #1463ff;
}

.message-bubble strong {
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
}

.message-bubble p {
  margin: 0;
  overflow-wrap: anywhere;
  font-size: 14px;
  line-height: 1.45;
}

.chat-composer {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid #e6ebf2;
}

.btn {
  height: 40px;
  padding: 0 16px;
  border: 0;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.primary-btn {
  color: #ffffff;
  background: #1463ff;
}

.secondary-btn {
  color: #172033;
  background: #eef2f7;
}

.chat-error {
  margin: 0;
  padding: 0 20px 16px;
  color: #c62828;
  font-size: 14px;
}

@media (max-width: 700px) {
  .chat-page {
    padding: 0;
  }

  .chat-shell {
    min-height: calc(100vh - 60px);
    border-width: 0;
    border-radius: 0;
  }

  .chat-header,
  .share-panel,
  .chat-composer {
    flex-direction: column;
    align-items: stretch;
  }

  .message-bubble {
    max-width: 88%;
  }
}
</style>
