contract ManagerContract {

	struct Comsumer {
		address addr;
		uint balance;
	}

	struct Transaction {
		Comsumer consumer;
		uint dt_start;
		uint dt_end;
		uint cost;
		uint256 hash_id;
	}

	struct Owner {
		address addr;
	}

	struct Sensor {
		uint sensor_id;
		uint dt_start;
		uint dt_end;
		uint fee;
	}

	Owner owner;

	mapping (uint => Sensor) sensors;
	mapping (address => Transaction) transactions;

	function ManagerContract() {
		owner = msg.sender;
	}

	function createSensor(uint sensor_id, uint fee, uint dt_start) returns (bool) {
		sensors[sensor_id].sensor_id = sensor_id;
		sensors[sensor_id].dt_start = dt_start;
		sensors[sensor_id].dt_end = dt_start;
		sensors[sensor_id].fee = fee
		return true;
	}

	function createData(uint sensor_id, uint timestamp) returns (bool) {
		Sensor sensor = sensors[sensor_id];
		sensor.dt_end = timestamp;
		return true;
	}

	function performTransaction (address who, uint256 hash_id) returns (bool) {
		
		if (msg.sender != owner) {
			return false;
		}

		Transaction transaction = transactions[who];

		transaction.consumer.balance = transaction.consumer.balance - transaction.cost;

		owner.send(transaction.cost)

		if (transaction.consumer.balance != 0) {
			transaction.consumer.addr.send(transaction.consumer.balance);
		}

		delete transactions[who];

		return true;
	}

	function holdTransaction(uint sensor_id, uint start_time, uint end_time) returns (uint256)  {
		Sensor sensor = sensors[sensor_id];
		if (end_time < start_time) {
			return false;
		}

		if (sensor.dt_start > start_time || sensor.dt_end < end_time) {
			return false;
		}

		uint cost = (end_time - start_time) * sensor.fee;

		if (cost > msg.value) {
			return false;
		}

		transactions[msg.sender].consumer.address = msg.sender;
		transactions[msg.sender].consumer.balance = msg.value;
		transactions[msg.sender].dt_start = start_time;
		transactions[msg.sender].dt_end = end_time;
		transactions[msg.sender].cost = cost;

		uint256 hash_id = sha3(msg.sender + dt_start + dt_end); //Check it!

		transactions[msg.sender].hash_id = hash_id;

		return hash_id;
	}

	//Сделать у транзакций срок исполнения и проверку на устаревшие транзакции, если срок вышел, вернуть деньги
}