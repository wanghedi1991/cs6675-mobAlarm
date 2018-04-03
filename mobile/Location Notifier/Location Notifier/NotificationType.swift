//
//  NotificationType.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/25/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit
class NotificationType: Equatable{
    
    var name:String = ""
    var places:[Place] = []
    
    init(name: String, places:[Place]){
        self.name = name
        self.places = places
    }
    
    init(name:String) {
        self.name = name
    }
    
    static func ==(lhs: NotificationType, rhs: NotificationType) -> Bool {
        return lhs.name == rhs.name
    }
    
}
