<?php

class MyDB extends SQLite3 {
	function __construct() {
		$this->open('/var/www/html/database/database.sqlite');
		if (!$this->lastErrorCode()) {
			// 随便加密
			$passwd = md5(microtime(true));
			$this->query("UPDATE `users` SET password='$passwd'");
		}
		// var_dump($this->lastErrorMsg());
	}
}
new MyDB();