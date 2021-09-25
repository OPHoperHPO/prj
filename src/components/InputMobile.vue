<template>
  <div class="input-wrap">
    <input
      @keydown="onPhoneKeyDown"
      @input="onPhoneInput"
      @paste="onPhonePaste"
      @focus="focus"
      @focusout="unfocus"
      @change="inputChanged"
      :id="name"
      :value="value"
      class="form-input"
      type="tel"
    />
    <label :for="name" :class="{ active: value }" class="form-label"
      ><slot></slot
    ></label>
  </div>
</template>

<script>
export default {
  name: 'InputMobile',

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
      e.target.labels[0].classList.add('active')
      e.target.labels[0].classList.add('focus')
    },

    unfocus(e) {
      if (!e.target.value)
        e.target.labels[0].classList.remove('active')

      e.target.labels[0].classList.remove('focus')
    },

    getInputNumbersValue(input) {
      return input.value.replace(/\D/g, '');
    },

    onPhonePaste(e) {
      let input = e.target
      let inputNumbersValue = this.getInputNumbersValue(input)
      let pasted = e.clipboardData || window.clipboardData
      if (/\D/g.test(pasted?.getData('Text'))) 
        return input.value = inputNumbersValue
    },

    onPhoneInput(e) {
      let input = e.target
      let inputNumbersValue = this.getInputNumbersValue(input)
      let selectionStart = input.selectionStart
      let formattedInputValue = ''

      if (!inputNumbersValue)
        return input.value = ''

      if (input.value.length != selectionStart) {
        if (e.data && /\D/g.test(e.data))
          input.value = inputNumbersValue
        return
      }

      if ('789'.includes(inputNumbersValue[0])) {
        if (inputNumbersValue[0] == '9')  
          inputNumbersValue = '7' + inputNumbersValue

        input.maxLength = (inputNumbersValue[0] == '8') ? 17 : 18 
        let firstSymbols = (inputNumbersValue[0] == '8') ? '8' : '+7'

        formattedInputValue = input.value = firstSymbols + ' '
        if (inputNumbersValue.length > 1)
          formattedInputValue += '(' + inputNumbersValue.substring(1, 4)

        if (inputNumbersValue.length >= 5)
          formattedInputValue += ') ' + inputNumbersValue.substring(4, 7)

        if (inputNumbersValue.length >= 8)
          formattedInputValue += '-' + inputNumbersValue.substring(7, 9)

        if (inputNumbersValue.length >= 10)
          formattedInputValue += '-' + inputNumbersValue.substring(9, 11)

      } else {
        formattedInputValue = '+' + inputNumbersValue.substring(0, 16)
        input.maxLength = 20
      }
      input.value = formattedInputValue
    },

    onPhoneKeyDown(e) {
      let input = e.target
      let inputValue = input.value.replace(/\D/g, '')
      if (e.keyCode == 8 && inputValue.length == 1)
        return input.value = ''
    },
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
  padding: 10px;
  padding-top: 22px;
  width: 100%;
  height: 100%;
  max-height: 55px;
  font: 16px "Roboto" 500;
  outline: none;
  border: solid 1px #dde1e6;
  border-radius: 4px;
  transition: border 0.2s ease-in-out;

  &:hover {
    border: solid 1px #b4bbc3;
  }

  &:focus {
    border: solid 1px #6eaffe;
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
    left: 12px;
  }

  &.focus {
    color: #6eaffe;
  }
}
</style>