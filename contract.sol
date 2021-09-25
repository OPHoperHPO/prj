// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

contract Contract {

    address public userAddress;  // Адрес клиента в блокчейне
    address public bankAddress;  // Адрес банка в блокчейне
    address public insCompAddress;  // Адрес страховой в блокчейне

    bool private is_active;  // Действует ли контракт
    bool private is_expired;  // Истёк ли контракт по дате

    // Данные об договоре
    string public bankName; // Название банка
    string public insCompName; // Название страховой компании
    string private userFullname; // ФИО
    uint256 private creditContractNumber; // Номер кредитного договора
    uint256 private creditContractTimestamp; //Дата кредитного договора в UNIX timestamp
    uint256 private contractNumber; // Номер договора страхования
    uint256 private contractTimestamp; // Дата договора страхования
    uint256 private totalAmount; // Страховая сумма
    uint256 private paymentTimestamp; // Дата оплаты
    uint256 private paymentAmount; // Сумма оплаты
    uint256 private indebtednessAmount; // Задолжность по оплате
    uint256 private indebtednessDate; // Дата закрытия кредита
    uint256 private contractRisks; // Страховые риски: вероятность от 0 до 1000000
    string private contractRisksType; // Страховые риски: тип

    InsuranceCaseContract public insuranceContract; // Контракт страхового случая.

    event ContractCreated(address indexed contractAddress, uint256 timestamp);  // контракт создался (Выставлен счёт на оплату)
    event ContractActivated(address indexed contractAddress, uint256 timestamp); // контракт активирован
    event ContractDeactivated(address indexed contractAddress, uint256 timestamp); // контракт деактивирован


    constructor(address bank, address user,
                string memory _bankName,
                string memory _insCompName,
                string memory luserFullname,
                uint256  lcreditContractNumber,
                uint256  lcreditContractTimestamp,
                uint256  lcontractNumber,
                uint256  ltotalAmount,
                string memory lcontractRisksType) {

        // Вносим инфу о договоре
        insCompName = _insCompName;
        bankName = _bankName;
        userFullname = luserFullname;
        creditContractTimestamp = lcreditContractTimestamp;
        creditContractNumber = lcreditContractNumber;
        totalAmount = ltotalAmount;
        contractRisksType = lcontractRisksType;
        contractNumber = lcontractNumber;
        contractTimestamp = block.timestamp;

        bankAddress = bank;
        userAddress = user;
        insCompAddress = msg.sender;   // Страховая создаёт договор
        emit ContractCreated(address(this), block.timestamp); // договор создан, но не активирован до оплаты. Шлём уведомление банку.


    }

    modifier isBank() {
        require(msg.sender == bankAddress, "Caller is not bank");
        _;
    }

    modifier isInsCompany() {
        require(msg.sender == insCompAddress, "Caller is not Ins Company");
        _;
    }

    modifier isUser() {
        require(msg.sender == userAddress, "Caller is not user");
        _;
    }

    modifier isUserOrInsCompany(){
        require(msg.sender == userAddress || msg.sender == insCompAddress, "Caller is not user or Ins Company");
        _;
    }


    modifier isUserOrBankOrInsCompany(){
        require(msg.sender == userAddress || msg.sender == insCompAddress || msg.sender == bankAddress, "Caller is not user or Ins Company");
        _;
    }

    function isActive() external view isUserOrBankOrInsCompany returns(bool){
        return(is_active);
    }
    function isExpired() external view isUserOrBankOrInsCompany returns(bool){
        return(is_expired);
    }

    function indebtednessUpdate(uint256 amount, uint256 endTimestamp) public isBank {
        require(is_active, "Contract should be active");
        require(!is_expired, "Contract expired");
        indebtednessAmount = amount;
        indebtednessDate = endTimestamp;
    }

    function getContractInfo() external view isUserOrBankOrInsCompany returns(
    bool,
    bool,
    string memory,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    uint256,
    string memory
    ){
        return(
        is_active,
        is_expired,
        userFullname,
        creditContractNumber,
        creditContractTimestamp,
        contractNumber,
        contractTimestamp,
        totalAmount,
        paymentTimestamp,
        paymentAmount,
        indebtednessAmount,
        indebtednessDate,
        contractRisks,
        contractRisksType

);
    }

    function getContractAddresses() external view isUserOrBankOrInsCompany returns(
    address,
    address,
    address,
    address


    ){
        return(
        userAddress,
        bankAddress,
        insCompAddress,
        address(insuranceContract)

);
    }

    function createInsurnanceCase(
        string memory reason, // Причина страхового случая
        string memory condition, // Обстоятельства страхового случая
        string memory phoneNumber, // Номер заявителя
        string memory  email, //  Email заявителя
        uint256 damageAmount,
        uint256 damageDate) public isUser {

        require(is_active, "Contract is deactivated");
        require(!is_expired, "Contract is expired");

        insuranceContract = new InsuranceCaseContract(
            address(this), reason, condition, phoneNumber, email, damageAmount, damageDate);
    }

    // Деактивирует контракт по запросу пользователя или страховой компании
    function deactivateContract() public isUserOrInsCompany {
        require(is_active, "Contract is already inactive");
        require(!is_expired, "Contract is expired");

        is_active = false;
        is_expired = true;  // Запрещаем реактивацию договора
        emit ContractDeactivated(address(this),  block.timestamp);
    }

    // Функция для банка для уведомления об оплате счёта
    function setPaymentRecieved(uint256 payment_timestamp, uint256 payment_amount) public isBank {
        require(!is_active, "Contract is already active");
        require(!is_expired, "Contract is expired");

        paymentAmount = payment_amount;
        paymentTimestamp = payment_timestamp;
        is_active = true;

        emit ContractActivated(address(this), block.timestamp);
    }

}

contract InsuranceCaseContract{
    Contract private _parentContractAddress; // Связанный договора о страховании
    string private _reason; // Причина страхового случая
    string private _condition; // Обстоятельства страхового случая
    string private _phoneNumber; // Номер заявителя
    string private _email; //  Email заявителя
    uint256 private _happenedDate; // Дата страхового события в UNIX timestamp
    uint256 private _damageAmount; // Размер ущерба страхового случая
    bool private _isPaymentConfirmed; // Подтверждёна ли выплата по обращению
    bool private _isClosed; // Закрыто ли обращение
    uint256 private _paymentAmount; // Выплата по страховому случаю.
    bool private _isPaymentConfirmedByBank; // Подтверждена ли выплата клиенту со стороны банка
    string private _rejectCause; // Причина отказа в выплате

    event InsuranceCaseConfirmed(address indexed contractAddress, uint256 timestamp); // Получено разрешение на выплату компенсации
    event InsuranceCaseCreated(address indexed contractAddress, uint256 timestamp); // Зарегистрировано страховое обращение
    event InsuranceCaseClosedRejected(address indexed contractAddress, uint256 timestamp, string cause); // Обращение закрыто и отклонено
    event InsuranceCaseClosedConfirmed(address indexed contractAddress, uint256 timestamp); // Обращение закрыто и выплачена компенсация
    event InsuranceCaseUpdated(address indexed contractAddress, uint256 timestamp); // Страховое обращение обновлено

    mapping (address => bool) isParent;

    constructor(
        address parentAddress,
        string memory reason, // Причина страхового случая
        string memory condition, // Обстоятельства страхового случая
        string memory phoneNumber, // Номер заявителя
        string memory  email, //  Email заявителя
        uint256 damageAmount,
        uint256 damageDate) public {

        Contract parentContract = Contract(parentAddress);
        isParent[parentAddress] = true;
        require(isParent[msg.sender], "Only parent contract can create this contract");

        _parentContractAddress = parentContract;
       _reason = reason;
       _condition = condition;
       _damageAmount = damageAmount;
       _happenedDate = damageDate;
       _email = email;
       _phoneNumber = phoneNumber;

       _isPaymentConfirmed = false;
       _paymentAmount = 0;
       _isClosed = false;
       emit InsuranceCaseCreated(address(this),  block.timestamp);
    }

    modifier isBank() {
        require(msg.sender == _parentContractAddress.bankAddress(), "Caller is not bank");
        _;
    }

    modifier isInsCompany() {
        require(msg.sender == _parentContractAddress.insCompAddress(), "Caller is not Ins Company");
        _;
    }

    modifier isUser() {
        require(_parentContractAddress.userAddress() == msg.sender, "Caller is not user");
        _;
    }

    modifier isUserOrInsCompany(){
        require(msg.sender == _parentContractAddress.userAddress() || msg.sender == _parentContractAddress.insCompAddress(), "Caller is not user or Ins Company");
        _;
    }


    modifier isUserOrBankOrInsCompany(){
        require(msg.sender == _parentContractAddress.userAddress() || msg.sender == _parentContractAddress.insCompAddress()
            || msg.sender == _parentContractAddress.bankAddress(),
            "Caller is not user or Ins Company or Bank");
        _;
    }



    function getInfo() external view isUserOrBankOrInsCompany
    returns(address, string memory, string memory,
        string memory, string memory,
    uint256, uint256, bool, bool, uint256, bool, string memory)  {
        return(address(_parentContractAddress),
        _reason, _condition, _phoneNumber,
                _email, _happenedDate, _damageAmount,
        _isPaymentConfirmed, _isClosed, _paymentAmount,
        _isPaymentConfirmedByBank, _rejectCause);
    }

    function closeReject(string memory cause) public isInsCompany {
        require(!_isClosed, "Contract is already closed");
        _isClosed = true;
        _rejectCause = cause;
        emit InsuranceCaseClosedRejected(address(this), block.timestamp, cause);

    }

    function confirmPaymentFromBank() public isBank {
        require(!_parentContractAddress.isExpired() && _parentContractAddress.isActive(),
            "Parent Contract is deactivated or expired");
        require(!_isClosed, "Contract deactivated");

        _isPaymentConfirmedByBank = true;
        _isClosed = true; // Закрываем обращение по причине подтверждения выплаты клиенту компенсации со стороны банка
        emit InsuranceCaseClosedConfirmed(address(this), block.timestamp);
    }

    function confirm(uint256 payment_amount) public isInsCompany  {
        require(!_parentContractAddress.isExpired() && _parentContractAddress.isActive(),
            "Parent Contract is deactivated or expired");
        require(!_isClosed, "Contract deactivated");

        _isPaymentConfirmed = true;
        _paymentAmount = payment_amount; // Страховая назначает свой размер компенсации
        emit InsuranceCaseConfirmed(address(this), block.timestamp);
        // Даём банку знать о том, что подтверждён страховой случай, а значит он должен обновить информацию о задолжности в этот момент
        // Обработать платёж и подтвердить выплату компенсации клиенту.
    }

    function update(
        string memory reason, // Причина страхового случая
        string memory condition, // Обстоятельства страхового случая
        string memory phoneNumber, // Номер заявителя
        string memory  email, //  Email заявителя
        uint256 damageAmount,
        uint256 damageDate) public isInsCompany {
        require(!_parentContractAddress.isExpired() && _parentContractAddress.isActive(),
            "Parent Contract is deactivated or expired");
        require(!_isClosed, "Contract deactivated");

       _reason = reason;
       _condition = condition;
       _damageAmount = damageAmount;
       _happenedDate = damageDate;
       _email = email;
       _phoneNumber = phoneNumber;

       emit InsuranceCaseUpdated(address(this),  block.timestamp);
        }

}