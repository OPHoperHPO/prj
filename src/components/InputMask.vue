<template>
  <div class="input-wrap">
    <input
      @focus="focus"
      @focusout="unfocus"
      @input="$emit('update:modelValue', $event.target.value)"
      :id="name"
      :type="type"
      :value="modelValue"
      class="form-input"
    />
    <label :for="name" :class="{ active: value }" class="form-label">
      <slot></slot>
    </label>
  </div>
</template>

<script>
export default {
  name: 'InputMask',

  props: {
    name: {
      type: String,
      required: true
    },
    modelValue: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: 'text'
    }
  },

  emits: ['update:modelValue'],

  methods: {
    focus(e) {
      e.target.labels[0].classList.add('active')
      e.target.labels[0].classList.add('focus')
    },

    unfocus(e) {
      if (!e.target.value) {
        e.target.labels[0].classList.remove('active')
      }

      e.target.labels[0].classList.remove('focus')
    }
  }
}
</script>

<style lang="scss" scoped>
* {
  cursor: text;
}

.input-wrap {
  margin: 15px auto;
  position: relative;
  width: 100%;
  max-height: 30%;

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

.form-input {
  padding: 22px 16px 10px;
  width: 100%;
  height: 100%;
  max-height: 55px;
  font: 16px "Roboto" 500;
  outline: none;
  border: solid 1px #dde1e6;
  border-radius: 1em;
  transition: border 0.2s ease-in-out;

  &:hover {
    border: solid 1px #b4bbc3;
  }

  &:focus {
    border: solid 1px var(--secondary);
  }
}

.form-label {
  position: absolute;
  color: #848e99;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  transition: all 0.2s ease-in-out;
  pointer-events: none;

  &.active {
    font-size: 12px;
    top: 12px;
    // left: 12px;
  }

  &.focus {
    color: var(--secondary);
  }
}
</style>