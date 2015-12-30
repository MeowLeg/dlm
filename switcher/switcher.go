package switcher

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"net/http"
	"time"
)

type Xl map[string]func(*http.Request) (string, interface{})

type Weixin struct {
	Id      int    `json:"id"`
	Href    string `json:"href"`
	Title   string `json:"title"`
	Img     string `json:"img"`
	Logdate string `json:"date"`
	Key     string `json:"key"`
}

func Dispatch(db *sql.DB) Xl {
	return Xl{

		"authorize": func(r *http.Request) (string, interface{}) {
			return "获取成功", map[string][][]string{
				"tokens": [][]string{
					[]string{"oIWsFtzlRvsDVd2e69iSjjYcTbW8", "舟山广电"},
					[]string{"oIWsFt0JFB3-dVvN7xqgLwG7lTZQ", "汪大姐来了"},
					[]string{"oIWsFt_90Pc5J5qYypXzgI9E11Rs", "讲拨侬听"},
					[]string{"oIWsFt5bh4aAeUwAgsLrGjBke2A0", "新闻综合频道"},
					[]string{"oIWsFt1OUb1JyTvY7AVBizjd4F-w", "公共生活频道"},
					[]string{"oIWsFtyXxULy9FfmEMrpYoo0Rxu4", "群岛旅游频道"},
					[]string{"oIWsFt8cgf4W8lutaRBM-4jC0nEA", "新闻998频率"},
					[]string{"oIWsFt-QtI5IGCGtE1Uc46aj0WZI", "交通97频率"},
					[]string{"oIWsFt_HcL1-Bt57PtLs3NZbAYo8", "汽车音乐频率"},
					[]string{"oIWsFt232h6j4SHUooOXzc1wcaXs", "电视新周报"},
				},
			}
		},

		"getWeixins": func(r *http.Request) (string, interface{}) {
			d, err := GetParameterWithError(r, "date")
			if err != nil {
				d = today()
			}
			rows, err := db.Query("select distinct strftime('%Y-%m-%d', logdate) from weixin where logdate <= ? and key = ? order by logdate desc limit 5", d, GetParameter(r, "key"))
			perror(err, "查询日期失败")
			var logdates []string
			for rows.Next() {
				var lg string
				rows.Scan(&lg)
				logdates = append(logdates, lg)
			}

			ret := make([]map[string][]Weixin, 0)
			for _, d := range logdates {
				rows, err := db.Query("select id, href, title, img, strftime('%Y-%m-%d', logdate), key from weixin where key = ? and logdate = ?", GetParameter(r, "key"), d)
				perror(err, "无法获取微信信息")
				var wxs []Weixin
				for rows.Next() {
					var wx Weixin
					rows.Scan(&wx.Id, &wx.Href, &wx.Title, &wx.Img, &wx.Logdate, &wx.Key)
					wxs = append(wxs, wx)
				}
				ret = append(ret, map[string][]Weixin{
					d: wxs,
				})
			}

			return "获取微信信息成功", ret
		},
	}
}

func GetParameter(r *http.Request, key string) string {
	s := r.URL.Query().Get(key)
	if s == "" {
		panic("没有参数" + key)
	}
	return s
}

func GetParameterWithError(r *http.Request, key string) (string, error) {
	s := r.URL.Query().Get(key)
	var err error
	if s == "" {
		err = errors.New("没有参数" + key)
	}
	return s, err
}

func perror(err error, msg string) {
	if err != nil {
		log.Println(msg)
		panic(err)
	}
}

func today() string {
	return time.Now().Format("2006-01-02")
}

func tommorrow() string {
	return time.Unix(time.Now().Unix()+86400, 0).Format("2006-01-02")
}
