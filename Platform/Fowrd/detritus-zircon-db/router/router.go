package router

import (
	"detritus-zircon-db/services"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// 支持跨域请求
	r.Use(cors.Default())
	zircon := r.Group("/zircon")
	{
		zircon.POST("/locations/bbox", services.GetOneData)
	}

	return r
}
