//
//  tableHolderController.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/25/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit
class TableHolderController: UITabBarController, UITabBarControllerDelegate {

    var notificationTypes:[NotificationType] = [Constant.testType0, Constant.testType1, Constant.testType2]
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.navigationItem.title = "Notification Categories"
        self.delegate = self
    }
    
    func tabBarController(_ tabBarController: UITabBarController, didSelect viewController: UIViewController) {
        print(String(self.selectedIndex))
        if self.selectedIndex == 0 {
            (viewController as! FirstViewController).setNavigationBar()
        } else if selectedIndex == 1 {
            (viewController as! SecondViewController).setNavigationBar()
        }
    }
   

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    

}
