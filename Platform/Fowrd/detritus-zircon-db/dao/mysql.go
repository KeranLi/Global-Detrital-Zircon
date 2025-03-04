package dao

import (
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
	"sync"
	"time"
)

var (
	db   *gorm.DB
	once sync.Once
)

const (
	MySQLUser     = "user"
	MySQLPassword = "Fcanhuan.27515"
	MySQLAddr     = "124.71.206.204:3306"
	MySQLDatabase = "zircon"
	//MySQLUser       = "user"
	//MySQLPassword   = "YMeIblT.jRciKLWkB0RL"
	//MySQLAddr       = "127.0.0.1:3306"
	//MySQLDatabase   = "onedz"
	MaxIdleConns    = 5                //最大空闲连接数
	MaxOpenConns    = 50               //最大连接数
	ConnMaxLifetime = 30 * time.Minute //连接可复用的最大时间
)

func initDB() {
	var err error
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8mb4&parseTime=True&loc=Local", MySQLUser, MySQLPassword, MySQLAddr, MySQLDatabase)
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("failed to connect database")
	}
	sqlDB, err := db.DB()
	if err != nil {
		log.Fatal("failed to get sql.DB")
	}
	// 设置连接池参数
	sqlDB.SetMaxIdleConns(MaxIdleConns)
	sqlDB.SetMaxOpenConns(MaxOpenConns)
	sqlDB.SetConnMaxLifetime(ConnMaxLifetime)
}

func InitDB() {
	once.Do(initDB)
}

func GetDB() *gorm.DB {
	return db
}
