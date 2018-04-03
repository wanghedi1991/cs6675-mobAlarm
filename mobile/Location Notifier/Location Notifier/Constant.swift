//
//  Constant.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/25/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit
struct Constant{
    static let studentCenter:Place = Place(name: "Student Center", latitude: 33.775262, longitude: -84.398768)
    static let klaus:Place = Place(name: "Klaus", latitude: 33.777310, longitude: -84.396213)
    static let coc:Place = Place(name: "CoC", latitude: 33.777805, longitude: -84.397415)
    static let crc:Place = Place(name: "Crc", latitude: 33.775780, longitude: -84.403938)
    
    static let testType0:NotificationType = NotificationType(name: "type 0", places: [studentCenter])
    static let testType1:NotificationType = NotificationType(name: "type 1", places: [klaus])
    static let testType2:NotificationType = NotificationType(name: "type 2", places: [coc, crc])
    static let allTypes:[NotificationType] = [Constant.testType0,Constant.testType1,Constant.testType2]
}


