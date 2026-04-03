<template>
  <div class="container mt-5">
    <div class="card shadow p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">My Offer Letters</h2>

        <button
          class="btn btn-secondary"
          @click="$router.push('/student-lobby')"
        >
          Back
        </button>
      </div>

      <div
        v-if="offerLetters.length === 0"
        class="text-center text-muted py-5"
      >
        No offer letters available yet.
      </div>

      <div
        v-for="offer in offerLetters"
        :key="offer.application_id"
        class="card mb-4 border-0 shadow-sm"
      >
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <h4 class="mb-1">{{ offer.job_title }}</h4>
              <h6 class="text-muted mb-0">{{ offer.company_name }}</h6>
            </div>

            <span class="badge bg-success fs-6">
              Offer Sent
            </span>
          </div>

          <div
            v-if="offer.message"
            class="alert alert-light border mb-3"
          >
            <strong>Message from Company:</strong><br>
            {{ offer.message }}
          </div>

          <button
            class="btn btn-primary"
            @click="downloadOfferLetter(offer.download_url)"
          >
            Download Offer Letter
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "StudentOfferLetter",

  data() {
    return {
      offerLetters: []
    }
  },

  mounted() {
    this.fetchOfferLetters()
  },

  methods: {
    async fetchOfferLetters() {
      try {
        const student = JSON.parse(localStorage.getItem("student"))

        const response = await axios.get(
          `http://127.0.0.1:5000/student/offer-letters/${student.id}`
        )

        this.offerLetters = response.data
      } catch (error) {
        alert("Failed to load offer letters")
      }
    },

    downloadOfferLetter(url) {
      window.open(url, "_blank")
    }
  }
}
</script>
