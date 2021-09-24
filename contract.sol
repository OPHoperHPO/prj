// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;



contract Contract {

    address private userAddress;  // Адрес клиента в блокчейне
    address public bankAddress;  // Адрес банка в блокчейне
    address public insCompAddress;  // Адрес страховой в блокчейне
    
    bool private is_active;  // Действует ли контракт
    bool private is_expired;  // Истёк ли контракт по дате
    
    // Данные об договоре
    string private userFullname; // ФИО
    uint256 private creditContractNumber; // Номер кредитного договора
    uint256 private creditContractTimestamp; //Дата кредитного договора в UNIX timestamp
    uint256 private contractNumber; // Номер договора страхования 
    uint256 private contractTimestamp; // Дата договора страхования
    uint256 private totalAmount; // Страховая сумма
    uint256 private paymentTimestamp; // Дата оплаты
    uint256 private paymentAmount; // Сумма оплаты
    uint256 private contractRisks; // Страховые риски: вероятность от 0 до 1000000
    string private contractRisksType; // Страховые риски: тип

    event ContractCreated(address indexed contractAddress);  // контракт создался (Выставлен счёт на оплату)
    event ContractActivated(address indexed contractAddress); // контракт активирован
    event ContractDeactivated(address indexed contractAddress); // контракт активирован
    event OwnerSet(address indexed oldOwner, address indexed newOwner);

    constructor(address bank, address user,     
                string memory luserFullname,
                uint256  lcreditContractNumber,
                uint256  lcreditContractTimestamp,
                uint256  lcontractNumber, 
                uint256  ltotalAmount, 
                string memory lcontractRisksType) {
                    
        // Вносим инфу о договоре
        userFullname = luserFullname;
        creditContractTimestamp = lcreditContractTimestamp;
        creditContractNumber = lcreditContractNumber;
        totalAmount = ltotalAmount;
        contractRisksType = lcontractRisksType;
        contractNumber = lcontractNumber;
        
        bankAddress = bank;
        userAddress = user;
        insCompAddress = msg.sender;   // Страховая создаёт договор
        emit ContractCreated(address(this)); // договор создан, но не активирован до оплаты. Шлём уведомление банку.
        
        
    }

    modifier isBank() {
        require(msg.sender == bankAddress, "Caller is not bank");
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
    
    function getContractData() public isUserOrBankOrInsCompany() returns(
    address, address,
    bool,bool, string memory, uint256, uint256, uint256, uint256,
    uint256, uint256,uint256,uint256, string memory){
        return(
        bankAddress, 
        insCompAddress, 
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
        contractRisks, 
        contractRisksType

);
    }
    
    // Деактивирует контракт по запросу пользователя или страховой компании
    function deactivateContract() public isUserOrInsCompany {
        require(is_active, "Contract is already inactive");
        require(!is_expired, "Contract is expired");
        
        is_active = false;  
        is_expired = true;  // Запрещаем реактивацию договора
    }

    // Функция для банка для уведомления об оплате счёта
    function setPaymentRecieved(uint256 payment_timestamp, uint256 payment_amount) public isBank {
        require(!is_active, "Contract is already active");
        require(!is_expired, "Contract is expired");
        
        paymentAmount = payment_amount;
        paymentTimestamp = payment_timestamp;
        is_active = true;
        
        emit ContractActivated(address(this));
    }
    
    
    // function getOwner() external view returns (address) {
    //     return owner;
    // }
    
    
}
