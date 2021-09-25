<template>
  <div class="area-wrap">
    <textarea
      @focus="focus"
      @focusout="unfocus"
      @change="inputChanged"
      :name="name"
      :id="name"
      :value="value"
      class="form-text"
    ></textarea>
    <label :for="name" :class="{ active: value }" class="area-label"
      ><slot></slot
    ></label>
  </div>
</template>

<script>
export default {
  name: 'InputArea',

  props: {
    name: {
      type: String,
      required: true
    },
    value: {
      required: true,
    },
  },

  methods: {
    inputChanged(e) {
      this.$emit('change', e.target.value, this.name)
    },

    focus(e) {
      e.target.parentElement.lastChild.classList.add('active')
      e.target.parentElement.lastChild.classList.add('focus')
    },

    unfocus(e) {
      if (!e.target.value) {
        e.target.parentElement.lastChild.classList.remove('active')
      }

      e.target.parentElement.lastChild.classList.remove('focus')
    }
  }
}
</script>

<style lang="scss" scoped>
* {
  cursor: text;
}

.area-wrap {
  margin: 15px auto;
  position: relative;
  width: 100%;

  &:first-child {
    margin-top: 0;
  }

  &.wrong {
    label {
      color: #ed414f;
    }
    input,
    textarea {
      border-color: #ed414f;
    }
  }
}

.form-text {
  padding: calc(1em + 12px) 12px 7px;
  min-height: calc(2em + 25px);
  height: 125px;
  max-height: 300px;
  width: 100%;
  border-radius: 4px;
  border: solid 1px #dde1e6;
  transition: border 0.2s ease-in-out;
  outline: none;
  resize: vertical;

  &:focus {
    border: solid 1px #6eaffe;
  }
}

.area-label {
  position: absolute;
  left: 20px;
  top: 20px;
  color: #848e99;
  cursor: text;
  transition: all 0.2s ease-in-out;

  &.active {
    font-size: 12px;
    top: 12px;
    left: 12px;
  }

  &.focus {
    color: #6eaffe;
  }
}
</style>