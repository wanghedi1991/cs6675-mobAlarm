//
//  SecondViewController.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/14/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit
import GoogleMaps

class SecondViewController: UIViewController, GMSMapViewDelegate, UITableViewDelegate, UITableViewDataSource {
    
    
    @IBOutlet weak var filterTable: UITableView!
    
    var filterShowing:Bool = false
    var mapView:GMSMapView = GMSMapView.init()
    var places:[Place] = []
    var types:[NotificationType] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let camera = GMSCameraPosition.camera(withLatitude: 33.777310, longitude: -84.396213, zoom: 14.0)
        mapView = GMSMapView.map(withFrame: CGRect(x:0,y:0,width:400,height:700), camera: camera)
        mapView.isMyLocationEnabled = true
        mapView.delegate = self
        self.view.addSubview(mapView)
        filterTable.isHidden = true
        filterTable.layer.zPosition = 3
        mapView.layer.zPosition = 2
        types = (self.tabBarController as! TableHolderController).notificationTypes

        for currentType in types {
            for currentPlace in currentType.places {
                if !places.contains(currentPlace){
                    places.append(currentPlace)
                }
            }
        }
        
        for currentPlace in places {
            var marker = GMSMarker()
            marker.position = CLLocationCoordinate2D(latitude: currentPlace.latitude, longitude: currentPlace.longitude)
            marker.title = currentPlace.name
            marker.map = mapView
        }
        
        self.filterTable.delegate = self
        self.filterTable.dataSource = self
        self.filterShowing = false
        
        
    }

    
    func setNavigationBar() {
         (self.tabBarController as! TableHolderController).navigationItem.rightBarButtonItem = UIBarButtonItem(title: "Filter", style: UIBarButtonItemStyle.plain, target: self, action: #selector(FilterButtonTapped))
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func mapView(_ mapView: GMSMapView, didTapInfoWindowOf marker: GMSMarker) {
        let latitude:Float = Float(marker.position.latitude)
        let longitude:Float = Float(marker.position.longitude)
        if (UIApplication.shared.canOpenURL(URL(string:"comgooglemaps://")!))
        {
            UIApplication.shared.openURL(NSURL(string:
                "comgooglemaps://?saddr=&daddr=\(Float(latitude)),\(Float(longitude))&directionsmode=driving")! as URL)
        } else
        {
            NSLog("Can't use com.google.maps://");
        }
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return types.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "mapFilterCell", for: indexPath) as! FilterCell
        cell.typeLabel.text = types[indexPath.row].name
        cell.accessoryType = UITableViewCellAccessoryType.checkmark
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableView.cellForRow(at: indexPath)?.accessoryType == UITableViewCellAccessoryType.checkmark {
            tableView.cellForRow(at: indexPath)?.accessoryType = UITableViewCellAccessoryType.none
            for curPlace in types[indexPath.row].places{
                if let index = places.index(of:curPlace) {
                    places.remove(at: index)
                }
            }
        } else {
            tableView.cellForRow(at: indexPath)?.accessoryType = UITableViewCellAccessoryType.checkmark
            for curPlace in types[indexPath.row].places{
                if !places.contains(curPlace){
                    places.append(curPlace)
                }
            }
        }
    }

    @IBAction func FilterButtonTapped(_ sender: UIBarButtonItem) {
        if filterShowing {
            sender.title = "filter"
            filterTable.isHidden = true
            mapView.frame = mapView.frame.offsetBy(dx: 0, dy: -200)
            filterShowing = false
            redrawMarkers()
        } else {
            sender.title = "Done"
            filterTable.isHidden = false
            mapView.frame = mapView.frame.offsetBy(dx: 0, dy: 200)
            filterShowing = true
        }
    }
    
    func redrawMarkers() {
        mapView.clear()
        for currentPlace in places {
            var marker = GMSMarker()
            marker.position = CLLocationCoordinate2D(latitude: currentPlace.latitude, longitude: currentPlace.longitude)
            marker.title = currentPlace.name
            marker.map = mapView
        }
    }
}

