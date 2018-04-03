//
//  FirstViewController.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/14/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UIPickerViewDataSource, UIPickerViewDelegate {

    @IBOutlet weak var typePicker: UIPickerView!
    @IBOutlet weak var notificationTypeTable: UITableView!
    var types:[NotificationType] = []
    var addList:[NotificationType] = [Constant.testType0, Constant.testType1, Constant.testType2]
    var tempType:Int = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let parentController = self.tabBarController as! TableHolderController
        types = parentController.notificationTypes
        
        self.notificationTypeTable.delegate = self
        self.notificationTypeTable.dataSource = self
        self.notificationTypeTable.tableFooterView = UIView()
        
        self.typePicker.dataSource = self
        self.typePicker.delegate = self
        setNavigationBar()
    }
    
    
    func setNavigationBar(){
        (self.tabBarController as! TableHolderController).navigationItem.rightBarButtonItem = UIBarButtonItem(title: "Add", style: UIBarButtonItemStyle.plain, target: self, action: #selector(addNotificationType))
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.types.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "notificationTypeCell", for: indexPath) as! NotificationTypeCell
        cell.nameLabel.text = types[indexPath.row].name
        return cell
    }
    
    func tableView(_ tableView: UITableView, editActionsForRowAt indexPath: IndexPath) -> [UITableViewRowAction]? {


        let deleteAction = UITableViewRowAction(style: .destructive, title: "Delete", handler: { (action, indexPath) in
            self.types.remove(at: indexPath.row)
            (self.tabBarController as! TableHolderController).notificationTypes.remove(at: indexPath.row)
            self.notificationTypeTable.reloadData()
        })
        deleteAction.backgroundColor = UIColor.red
        
        return [deleteAction]
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return addList.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return addList[row].name
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        self.tempType = row
    }
    
    
    @IBAction func addNotificationType(_ sender: UIBarButtonItem) {
     //   self.doneButton.isHidden = false
        if self.typePicker.isHidden {
            self.typePicker.isHidden = false
            self.notificationTypeTable.isHidden = true
            sender.title = "Done"
        } else {
            self.typePicker.isHidden = true
            self.notificationTypeTable.isHidden = false
            if self.types.contains(addList[tempType]) {
                showToast(message: "It is already added")
            } else {
                self.types.append(addList[tempType])
                (self.tabBarController as! TableHolderController).notificationTypes.append(addList[tempType])
                self.notificationTypeTable.reloadData()
            }
            sender.title = "Add"
        }
    }
    
}

extension UIViewController {
    
    func showToast(message : String) {
        
        let toastLabel = UILabel(frame: CGRect(x: self.view.frame.size.width/2 - 75, y: self.view.frame.size.height-100, width: 150, height: 35))
        toastLabel.backgroundColor = UIColor.black.withAlphaComponent(0.6)
        toastLabel.textColor = UIColor.white
        toastLabel.textAlignment = .center;
        toastLabel.font = UIFont(name: "Montserrat-Light", size: 12.0)
        toastLabel.text = message
        toastLabel.alpha = 1.0
        toastLabel.layer.cornerRadius = 10;
        toastLabel.clipsToBounds  =  true
        self.view.addSubview(toastLabel)
        UIView.animate(withDuration: 4.0, delay: 0.1, options: .curveEaseOut, animations: {
            toastLabel.alpha = 0.0
        }, completion: {(isCompleted) in
            toastLabel.removeFromSuperview()
        })
    }
}




