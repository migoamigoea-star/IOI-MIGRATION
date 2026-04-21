param(
    [Parameter(Mandatory = $true)]
    [string]$SiteUrl,
    [string]$ListName = "MainDB_STR",
    [int]$ReadSecurity = 1,
    [int]$WriteSecurity = 1
)

Import-Module PnP.PowerShell -ErrorAction Stop
Connect-PnPOnline -Url $SiteUrl -Interactive

$list = Get-PnPList -Identity $ListName -ErrorAction SilentlyContinue
if (-not $list) {
    New-PnPList -Title $ListName -Template GenericList -EnableVersioning $true -EnableAttachments $true
}
Set-PnPList -Identity $ListName -EnableVersioning $true -EnableAttachments $true -ReadSecurity $ReadSecurity -WriteSecurity $WriteSecurity
Set-PnPList -Identity $ListName -BreakRoleInheritance -CopyRoleAssignments

function Ensure-ListField {
    param(
        [string]$InternalName,
        [string]$DisplayName,
        [string]$Type,
        [bool]$Required,
        [string[]]$Choices
    )
    $existing = Get-PnPField -List $ListName -Identity $InternalName -ErrorAction SilentlyContinue
    if ($existing) {
        return
    }
    if ($Type -eq "Choice") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Choice -AddToDefaultView -Required:$Required -Choices $Choices
        return
    }
    if ($Type -eq "Multiple lines") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Note -AddToDefaultView -Required:$Required
        return
    }
    if ($Type -eq "Single line") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Text -AddToDefaultView -Required:$Required
        return
    }
    if ($Type -eq "Date and Time") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type DateTime -AddToDefaultView -Required:$Required
        return
    }
    if ($Type -eq "Person or Group") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type User -AddToDefaultView -Required:$Required
        return
    }
    if ($Type -eq "Currency") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Currency -AddToDefaultView -Required:$Required
        return
    }
    if ($Type -eq "Yes/No") {
        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Boolean -AddToDefaultView -Required:$Required
        return
    }
    Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type $Type -AddToDefaultView -Required:$Required
}

$fields = @(
    @{ InternalName = "FormCode"; DisplayName = "Form Code"; Type = "Single line"; Required = $true; Choices = @() }
    @{ InternalName = "INO"; DisplayName = "Inclusion Ref No"; Type = "Single line"; Required = $true; Choices = @() }
    @{ InternalName = "CurrentStatus"; DisplayName = "Workflow Status"; Type = "Choice"; Required = $true; Choices = @("Draft", "Submitted", "HODApproved", "MaterialsApproved", "FinanceApproved", "EDApproved", "Completed", "Rejected", "Discarded") }
    @{ InternalName = "CurrentAction"; DisplayName = "Current Action"; Type = "Choice"; Required = $true; Choices = @("Submit", "Review", "Approve", "Complete", "Discard") }
    @{ InternalName = "RequestDate"; DisplayName = "Request Date"; Type = "Date and Time"; Required = $true; Choices = @() }
    @{ InternalName = "Requestor"; DisplayName = "Requestor"; Type = "Person or Group"; Required = $true; Choices = @() }
    @{ InternalName = "RequestDept"; DisplayName = "Requesting Department"; Type = "Single line"; Required = $true; Choices = @() }
    @{ InternalName = "ItemDescription"; DisplayName = "Item Description"; Type = "Multiple lines"; Required = $true; Choices = @() }
    @{ InternalName = "ItemCategory"; DisplayName = "Item Category"; Type = "Choice"; Required = $true; Choices = @("Raw Material", "Packaging", "Spare", "Consumable", "Other") }
    @{ InternalName = "BuyerAssessment"; DisplayName = "Buyer Assessment"; Type = "Multiple lines"; Required = $false; Choices = @() }
    @{ InternalName = "EstimatedCost"; DisplayName = "Estimated Cost"; Type = "Currency"; Required = $false; Choices = @() }
    @{ InternalName = "TotalHoldingCost"; DisplayName = "Total Holding Cost"; Type = "Currency"; Required = $false; Choices = @() }
    @{ InternalName = "HODDecision"; DisplayName = "HOD Decision"; Type = "Choice"; Required = $false; Choices = @("Approved", "Rejected") }
    @{ InternalName = "MaterialsDecision"; DisplayName = "Materials Decision"; Type = "Choice"; Required = $false; Choices = @("Approved", "Rejected") }
    @{ InternalName = "FinanceDecision"; DisplayName = "Finance Decision"; Type = "Choice"; Required = $false; Choices = @("Approved", "Rejected") }
    @{ InternalName = "EDDecision"; DisplayName = "ED Decision"; Type = "Choice"; Required = $false; Choices = @("Approved", "Rejected") }
    @{ InternalName = "WarehouseDataComplete"; DisplayName = "Warehouse Data Complete"; Type = "Yes/No"; Required = $false; Choices = @() }
    @{ InternalName = "MRPDataComplete"; DisplayName = "MRP Data Complete"; Type = "Yes/No"; Required = $false; Choices = @() }
    @{ InternalName = "AccountingDataComplete"; DisplayName = "Accounting Data Complete"; Type = "Yes/No"; Required = $false; Choices = @() }
    @{ InternalName = "MaterialCode"; DisplayName = "Material Code"; Type = "Single line"; Required = $false; Choices = @() }
    @{ InternalName = "PRCreated"; DisplayName = "PR Created"; Type = "Yes/No"; Required = $false; Choices = @() }
    @{ InternalName = "DiscardFlag"; DisplayName = "Discard Flag"; Type = "Yes/No"; Required = $false; Choices = @() }
    @{ InternalName = "DiscardReason"; DisplayName = "Discard Reason"; Type = "Multiple lines"; Required = $false; Choices = @() }
    @{ InternalName = "SubmittedBy"; DisplayName = "Submitted By"; Type = "Person or Group"; Required = $true; Choices = @() }
    @{ InternalName = "SubmittedDate"; DisplayName = "Submitted Date"; Type = "Date and Time"; Required = $true; Choices = @() }
    @{ InternalName = "EnvironmentTag"; DisplayName = "Environment"; Type = "Choice"; Required = $true; Choices = @("DEV", "TEST", "PROD") }
    @{ InternalName = "IsLocked"; DisplayName = "Is Locked"; Type = "Yes/No"; Required = $false; Choices = @() }
)

foreach ($field in $fields) {
    Ensure-ListField -InternalName $field.InternalName -DisplayName $field.DisplayName -Type $field.Type -Required $field.Required -Choices $field.Choices
}

$roleAssignments = @(
    @{ GroupName = "D13-STR-Users"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-HOD-Reviewers"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-Materials"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-Finance"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-Executive-Approvers"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-MasterData"; PermissionLevel = "Contribute" }
    @{ GroupName = "D13-STR-Admins"; PermissionLevel = "Full Control" }
    @{ GroupName = "D13-STR-Readers"; PermissionLevel = "Read" }
)

foreach ($assignment in $roleAssignments) {
    $group = Get-PnPGroup -Identity $assignment.GroupName -ErrorAction SilentlyContinue
    if (-not $group) {
        $group = New-PnPGroup -Title $assignment.GroupName
    }
    Set-PnPGroupPermissions -Identity $assignment.GroupName -AddRole $assignment.PermissionLevel -List $ListName
}

Write-Host "[SII] SharePoint list provisioning completed for $ListName."