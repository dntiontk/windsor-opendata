package main

import (
	"fmt"
	"golang.org/x/net/html"
	"log"
	"net/http"
	"strings"
)

const src = "https://opendata.citywindsor.ca/Tools/CouncilAgendas?returnUrl=https://citywindsor.ca/cityhall/City-Council-Meetings/Pages/default.aspx"

func main() {
	resp, err := http.Get(src)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	doc, err := html.Parse(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	cards := getCards(doc)
	fmt.Printf("There are %d meetings found at %s\n\n", len(cards), src)
	for _, card := range cards {
		fmt.Println(card.Title)
		for _, link := range card.Links {
			if strings.Contains(link, "Agenda.pdf") {
				fmt.Printf("\t- %s\n", link)
			}
		}
	}
}

type Card struct {
	Title string
	Links []string
	*html.Node
}

func getCards(doc *html.Node) []Card {
	cards := make([]Card, 0)
	var fetchFn func(*html.Node)
	fetchFn = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "div" {
			for _, attr := range n.Attr {
				if attr.Val == "CA_CouncilAgenda 2024" {
					cards = append(cards, Card{
						Title: extractTitle(n),
						Links: extractLinks(n),
						Node:  n,
					})
					break
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			fetchFn(c)
		}
	}
	fetchFn(doc)
	return cards
}

func extractTitle(node *html.Node) string {
	var title string
	var fetchFn func(*html.Node)
	fetchFn = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "strong" {
			title = n.FirstChild.Data
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			fetchFn(c)
		}
	}
	fetchFn(node)
	return title
}

func extractLinks(node *html.Node) []string {
	links := make([]string, 0)
	var fetchFn func(*html.Node)
	fetchFn = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "a" {
			for _, attr := range n.Attr {
				if attr.Key == "href" {
					links = append(links, attr.Val)
					break
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			fetchFn(c)
		}
	}
	fetchFn(node)
	return links
}
