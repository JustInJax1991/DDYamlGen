$FilePath = ".\CamAssign.xlsx"
$excel = Import-Excel -Path $FilePath -WorksheetName "AT&T Pebble Beach" -HeaderName "Hole", "Tee", "Fairway1", "Fairway2", "Fairway3", "Fairway4", "Fairway5", "Fairway6", "Green1", "Green2", "Green3" -StartRow 3 -EndRow 20 -StartColumn 1 -EndColumn 11

$myArrayList = New-Object System.Collections.ArrayList

$i = 0

#get camera name sl1-b01
#iterate of $excel array    
while($i -lt $excel.count){
    $excel[$i].PSObject.Properties | foreach-object {


        $value = $_.value
        
        if($value.length -gt 1){
            #I am correcting the name to match what is in DNS, SL1-B121 for example
            $theIndex = $value.IndexOf('-')
            $value = $value.Insert($theIndex + 1, 'b')
            $hole = $excel[$i].Hole
            $location = $_.Name
            $myString = "${value},${hole},$location"
            #Build my PiList
            $myArrayList.add($myString)
            
            
        }
        
    }
    $i++
}

[pscustomobject]$os_list = (ConvertFrom-Yaml -yaml (get-content -Raw .\conf.yaml.template))

$tags = $os_list.instances

$myArray = New-Object System.Collections.ArrayList

foreach($tag in $tags){
  

    if($tag.tags.Contains("name:sl1-b01")){
        Write-Host "Enter"
        forEach($value in $tag.tags){
            
           if($value -like "hole*"){
                $value = "hole:1"
                $myArray.add($value)
                continue
            }
            $myArray.add($value)
        
        }
        continue
        
    }
    
}


$tags.tags >> test.yaml







$pi = Get-Content .\PI.txt
$ip = Get-Content .\IP.txt

$i = 0

while($i -lt $pi.length){

    $myString = $pi[$i].trimend("-Pi")
    $theIndex = $myString.IndexOf('-')
    $myString = $myString.Remove($theIndex, 1)
    $myString = "PI-" + $mystring + "," + "172.25.45." + $ip[$i]
    
    $myString >> PiIPSysListSL3.txt
    $i++

}





$theIndex = $value.IndexOf('-')
                    $value = $value.Insert($theIndex + 1, 'B')