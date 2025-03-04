package services

import (
	"bytes"
	"database/sql"
	"detritus-zircon-db/dao"
	"encoding/csv"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"gorm.io/gorm"
	"log"
	"net/http"
)

type requestBody struct {
	Bbox struct {
		MinLongitude float64 `json:"min_longitude" binding:"required"`
		MinLatitude  float64 `json:"min_latitude" binding:"required"`
		MaxLongitude float64 `json:"max_longitude" binding:"required"`
		MaxLatitude  float64 `json:"max_latitude" binding:"required"`
	} `json:"bbox" binding:"required"`
}

func GetOneData(c *gin.Context) {
	var (
		statusCode int
		resp       string
		err        error
	)

	// 读取并保存请求体
	//req, _ := io.ReadAll(c.Request.Body)
	//c.Request.Body = io.NopCloser(bytes.NewBuffer(req))
	defer func() {
		if err != nil {
			var req []byte
			if cb, ok := c.Get(gin.BodyBytesKey); ok {
				if cbb, ok := cb.([]byte); ok {
					req = cbb
				}
			}
			log.Printf("Response status code not 200, request:%s", string(req))
			c.String(statusCode, resp)
		}
	}()

	var body requestBody
	if err = c.ShouldBindBodyWith(&body, binding.JSON); err != nil {
		statusCode = http.StatusBadRequest
		resp = "invalid request body"
		return
	}
	if body.Bbox.MaxLatitude < body.Bbox.MinLatitude || body.Bbox.MaxLongitude < body.Bbox.MinLongitude {
		statusCode = http.StatusBadRequest
		resp = "invalid param"
		return
	}

	db := dao.GetDB()

	// 创建一个缓冲区用于保存CSV数据
	var buf bytes.Buffer
	writer := csv.NewWriter(&buf)
	defer writer.Flush()

	// 准备查询语句
	var rows *sql.Rows
	var result *gorm.DB
	result = db.Raw("SELECT * FROM zircon WHERE Latitude BETWEEN ? AND ? AND Longitude BETWEEN ? AND ?", body.Bbox.MinLatitude, body.Bbox.MaxLatitude, body.Bbox.MinLongitude, body.Bbox.MaxLongitude)
	rows, err = result.Rows()
	if err != nil {
		statusCode = http.StatusInternalServerError
		resp = "query failed"
		return
	}
	defer rows.Close()

	// 获取列名
	columns, err := rows.Columns()
	if err != nil {
		statusCode = http.StatusInternalServerError
		resp = "query failed"
		return
	}

	// 写入CSV头部
	if err := writer.Write(columns); err != nil {
		log.Fatal(err)
	}

	// 读取行数据
	for rows.Next() {
		// 创建一个切片用于保存每一行的数据
		valuePtrs := make([]interface{}, len(columns))
		values := make([]string, len(columns))

		// 初始化 sql.NullString 切片以处理 NULL 值
		nullStrings := make([]sql.NullString, len(columns))
		for i := range valuePtrs {
			valuePtrs[i] = &nullStrings[i]
		}

		// 扫描一行数据
		if err := rows.Scan(valuePtrs...); err != nil {
			statusCode = http.StatusInternalServerError
			resp = "row scan failed"
			return
		}

		// 将 NullString 转换为普通字符串，并构建最终的值列表
		for i, ns := range nullStrings {
			if ns.Valid {
				values[i] = ns.String
			} else {
				values[i] = "" // 使用空字符串表示 NULL
			}
		}

		// 写入CSV行数据
		if err := writer.Write(values); err != nil {
			statusCode = http.StatusInternalServerError
			resp = "data write failed"
			return
		}
	}

	// 检查遍历过程中是否有错误
	if err := rows.Err(); err != nil {
		statusCode = http.StatusInternalServerError
		resp = "rows scan failed"
		return
	}

	// 设置响应头
	c.Header("Content-Type", "text/csv")
	c.Header("Content-Disposition", "attachment; filename=data.csv")
	c.Header("File-Name", "data.csv")

	// 将CSV数据写入响应体
	c.Data(http.StatusOK, "text/csv", buf.Bytes())
}
