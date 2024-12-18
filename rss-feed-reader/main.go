package main

import (
	"crypto/tls"
	"encoding/xml"
	"flag"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const (
	feedUrl = "https://opendata.citywindsor.ca/RSS"

	alleyRepairFlooding     = "alley-repair-flooding"
	fenceHedgeConcerns      = "fence-hedge-concerns"
	garbage                 = "garbage"
	illegalDumping          = "illegal-dumping"
	landParcels             = "land-parcels"
	litterBin               = "litter-bin"
	parking                 = "parking"
	parksAndTrails          = "parks-and-trails"
	playgrounds             = "playgrounds"
	precipitation           = "precipitation"
	recycling               = "recycling"
	roadsAndSidewalks       = "roads-and-sidewalks"
	rodentExtermination     = "rodent-extermination"
	sewersAndManholes       = "sewers-and-manholes"
	skunkInspection         = "skunk-inspection"
	snowplow                = "snowplow"
	snowRemoval             = "snow-removal"
	streetCentreline        = "street-centreline"
	transitWindsorBusRoutes = "transit-windsor-bus-routes"
	treeRequest             = "tree-request"
	yardWaste               = "yard-waste"
	uncategorized           = "uncategorized"
)

var dataDir string

func main() {
	flag.StringVar(&dataDir, "dir", "raw", "specify the desination data directory")
	flag.Parse()

	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}

	resp, err := client.Get(feedUrl)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	var rss RSS
	if err := xml.Unmarshal(data, &rss); err != nil {
		log.Fatal(err)
	}

	categories := map[string]ItemList{
		alleyRepairFlooding:     make(ItemList, 0),
		fenceHedgeConcerns:      make(ItemList, 0),
		garbage:                 make(ItemList, 0),
		illegalDumping:          make(ItemList, 0),
		landParcels:             make(ItemList, 0),
		litterBin:               make(ItemList, 0),
		parking:                 make(ItemList, 0),
		parksAndTrails:          make(ItemList, 0),
		playgrounds:             make(ItemList, 0),
		precipitation:           make(ItemList, 0),
		recycling:               make(ItemList, 0),
		roadsAndSidewalks:       make(ItemList, 0),
		rodentExtermination:     make(ItemList, 0),
		sewersAndManholes:       make(ItemList, 0),
		skunkInspection:         make(ItemList, 0),
		snowplow:                make(ItemList, 0),
		snowRemoval:             make(ItemList, 0),
		streetCentreline:        make(ItemList, 0),
		transitWindsorBusRoutes: make(ItemList, 0),
		treeRequest:             make(ItemList, 0),
		yardWaste:               make(ItemList, 0),
		uncategorized:           make(ItemList, 0),
	}

	for _, item := range rss.Channel.Item {
		switch {
		case strings.Contains(item.Title, "SewersandManholes"), strings.Contains(item.Title, "Manholes"), strings.Contains(item.Title, "Sewer_"):
			categories[sewersAndManholes] = append(categories[sewersAndManholes], item)
		case strings.Contains(item.Title, "Land Parcels"):
			categories[landParcels] = append(categories[landParcels], item)
		case strings.Contains(item.Title, "Parks"), strings.Contains(item.Title, "Trails"):
			categories[parksAndTrails] = append(categories[parksAndTrails], item)
		case strings.Contains(item.Title, "snowplow"):
			categories[snowplow] = append(categories[snowplow], item)
		case isPrecipitationData(item.Title):
			categories[precipitation] = append(categories[precipitation], item)
		case strings.Contains(item.Title, "Transit Windsor Bus Routes"):
			categories[transitWindsorBusRoutes] = append(categories[transitWindsorBusRoutes], item)
		case strings.Contains(item.Title, "Street Centreline"), strings.Contains(item.Title, "Street Centerline"):
			categories[streetCentreline] = append(categories[streetCentreline], item)
		case strings.Contains(item.Title, "Playgrounds"):
			categories[playgrounds] = append(categories[playgrounds], item)
		case strings.Contains(item.Title, "Alley_Repair_"):
			categories[alleyRepairFlooding] = append(categories[alleyRepairFlooding], item)
		case strings.Contains(item.Title, "Fence_Hedge_Concerns"):
			categories[fenceHedgeConcerns] = append(categories[fenceHedgeConcerns], item)
		case strings.Contains(item.Title, "Yard_Waste"):
			categories[yardWaste] = append(categories[yardWaste], item)
		case strings.Contains(item.Title, "Tree_Request"):
			categories[treeRequest] = append(categories[treeRequest], item)
		case strings.Contains(item.Title, "Snow_"):
			categories[snowRemoval] = append(categories[snowRemoval], item)
		case strings.Contains(item.Title, "Skunk_"):
			categories[skunkInspection] = append(categories[skunkInspection], item)
		case strings.Contains(item.Title, "Sidewalk_"), strings.Contains(item.Title, "Sidewalks_"), strings.Contains(item.Title, "Shoulder_"), strings.Contains(item.Title, "Road_"):
			categories[roadsAndSidewalks] = append(categories[roadsAndSidewalks], item)
		case strings.Contains(item.Title, "Rodent_"):
			categories[rodentExtermination] = append(categories[rodentExtermination], item)
		case strings.Contains(item.Title, "Recycling_"):
			categories[recycling] = append(categories[recycling], item)
		case strings.Contains(item.Title, "Parking_"):
			categories[parking] = append(categories[parking], item)
		case strings.Contains(item.Title, "Litter_Bin"):
			categories[litterBin] = append(categories[litterBin], item)
		case strings.Contains(item.Title, "Illegal_Dumping"):
			categories[illegalDumping] = append(categories[illegalDumping], item)
		case strings.Contains(item.Title, "Garbage_"):
			categories[garbage] = append(categories[garbage], item)
		default:
			categories[uncategorized] = append(categories[uncategorized], item)
		}
	}

	for k, v := range categories {
		log.Printf("updating (%d) files for %s", len(v), k)
		for _, i := range v {
			fp := filepath.Join(dataDir, k, i.Title)
			out, err := os.Create(fp)
			if err != nil {
				log.Fatal(err)
			}
			defer out.Close()

			resp, err := client.Get(i.Link)
			if err != nil {
				log.Fatal(err)
			}
			defer resp.Body.Close()

			if _, err := io.Copy(out, resp.Body); err != nil {
				log.Fatal(err)
			}
		}
	}
	log.Println("complete")
}

type RSS struct {
	XMLName xml.Name `xml:"rss"`
	Text    string   `xml:",chardata"`
	Version string   `xml:"version,attr"`
	Media   string   `xml:"media,attr"`
	Channel Channel  `xml:"channel"`
}

type Channel struct {
	Text  string `xml:",chardata"`
	Title string `xml:"title"`
	Link  string `xml:"link"`
	Item  []Item `xml:"item"`
}

type Item struct {
	Text    string `xml:",chardata"`
	Title   string `xml:"title"`
	Link    string `xml:"link"`
	PubDate string `xml:"pubDate"`
}

type ItemList []Item

func isPrecipitationData(title string) bool {
	return title == "01 Ambassador.csv" ||
		title == "02 CMH Woods.csv" ||
		title == "03 Drouillard.csv" ||
		title == "04 East Banwell.csv" ||
		title == "05 Grand Marais.csv" ||
		title == "06 Howard Grade.csv" ||
		title == "07 Huron Estates.csv" ||
		title == "08 Lou Romano.csv" ||
		title == "09 Pillette.csv" ||
		title == "10 Pontiac.csv" ||
		title == "11 Provincial.csv" ||
		title == "12 Twin Oaks.csv" ||
		title == "13 Wellington.csv"
}
