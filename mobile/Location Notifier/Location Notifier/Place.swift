//
//  LocationEntity.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/25/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit
class Place: Equatable{
    static func ==(lhs: Place, rhs: Place) -> Bool {
        if lhs.latitude == rhs.latitude && lhs.longitude == rhs.longitude && lhs.name == rhs.name{
            return true
        }
        return false
    }
    
    var name:String = ""
    var longitude = 0.0
    var latitude = 0.0
    
    init(name: String, latitude: Double, longitude: Double) {
        self.name = name
        self.longitude  = longitude
        self.latitude = latitude
    }
    
}
