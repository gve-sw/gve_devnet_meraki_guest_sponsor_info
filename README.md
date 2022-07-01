# GVE DevNet Meraki Guest Sponsor Info
Cisco Meraki provides a cloud-managed network with rich functionality. One of these functionalities is a _Sponsored Guest Login_, which allows guests to authenticate wirelessly and request access to the wireless network. Through a splash page, they will have to specify a _sponsor_ from the corporate domain. The sponsor will receive a confirmation email and verify that the guest wants to connect to the guest network. While the Meraki Dashboard does provide reporting and CSV exports about the wireless network, at the time of writing the default CSV reports do not include information about the sponsor and when the authorization expires. However, this information is available in the Meraki Dashboard. This prototype shows how to obtain the information from the Meraki Dashboard and display the information in a CSV report through a Python script. 

The prototype Python script creates a CSV report in five steps:

1. Log in to the Meraki Dashboard

2. Select the organization and redirect to the Meraki Dashboard of the organization

3. Obtain the clients connected to the guest SSID

4. For each client, obtain the splash info and add it to the output JSON object

5. Convert from JSON to CSV and save the CSV report in output directory

![flow](IMAGES/flow.png)
![design](IMAGES/design.png)



## Contacts
* Simon Fang (sifang@cisco.com)

## Solution Components
* Python 3
* Meraki Dashboard
* Meraki MR

## Prerequisites
* Meraki Dashboard API Access enabled
* Sponsored Guest Flow enabled

## How to obtain a Meraki API Key

In order to use the Cisco Meraki API, you have to enable the API for your organization first. After having enabled API access, you can generate an API key. You can follow the following instructions on how to enable API access and how to generate an API key:

1. Log in to the Cisco Meraki dashboard

2. In the left-hand menu, go to `Organization > Settings > Dasbhoard API access`

3. Click on `Enable access to the Cisco Meraki Dashboard API`

4. Go to `Profile > API access`

5. Under `API access`, click on `Generate API key`

6. Save the API key in a safe place. Please note that the API key will be shown only once for security purposes. In case you lose the key, then you have to revoke the key and regenerate a new key. Moreover, there is a limit of only two API keys per profile. 

> For more information on how to generate an API key, please click here [here](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)

> Note: Make sure this API key has write access to the organization. You can add your account as Full Organization Admin to the organization by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

## How to enable the Sponsored Guest flow
The Sponsored Guest flow allows guests to wirelessly authenticate themselves and gain access to the network through a sponsor. The sponsor needs to verify the identity of the guest. In the following section, it will be explained how to enable this flow:

1. Administrators navigate to **Wireless > Access Control**. Scroll down to **Splash Page** and select **Sponsored guest login**.

2. Specify the allowed **sponsor email domains** and the **maximum sponsorship duration**.

3. Click **save**.

> For more information, please refer to the [documentation](https://documentation.meraki.com/MR/Encryption_and_Authentication/Sponsored_Guest)

## How to obtain the network ID
There are multiple ways to obtain the network ID. One of the ways is through the API documentation: 

1. Go to the Meraki API [documentation](https://developer.cisco.com/meraki/api-latest/)

2. Obtain the Meraki API key (instructions are in the previous section)

3. Navigate to **Endpoints > API > GENERAL > organizations > CONFIGURE > Get Organizations** and add the Meraki API key to `X-Cisco-Meraki-API-Key` in **Configuration**. 

4. Make the call to the `/organizations` endpoint by clicking on **Run**. 

5. Copy the `id` from the response with the correct `organization name`. 

6.  Navigate to **Endpoints > API > GENERAL > organizations > CONFIGURE > networks > Get Organization Networks**

7. Make a call to `/organizations/{organizationId}/networks` by adding the `organizationId` that you copied earlier and click on run

8. Copy the `id` from the response with the correct `network name`. 


## Installation/Configuration

The following commands are executed in the terminal.

1. Create and activate a virtual environment for the project:
   
        #WINDOWS:
        $ py -3 -m venv [add_name_of_virtual_environment_here] 
        $ [add_name_of_virtual_environment_here]/Scripts/activate.bat 
        #MAC:
        $ python3 -m venv [add_name_of_virtual_environment_here] 
        $ source [add_name_of_virtual_environment_here]/bin/activate
        
> For more information about virtual environments, please click [here](https://docs.python.org/3/tutorial/venv.html)

2. Access the created virtual environment folder

        $ cd [add_name_of_virtual_environment_here]

3. Clone this repository

        $ git clone [add_link_to_repository_here]

4. Access the folder `gve_devnet_meraki_guest_sponsor_info`

        $ cd gve_devnet_meraki_guest_sponsor_info

5. Install the dependencies:

        $ pip install -r requirements.txt

6. Open the `config.py` file and add the name of the organization, the network_id and the SSID name:

    ```python
    MERAKI_ORGANIZATION_NAME = "<insert_meraki_organization_name>"
    NETWORK_ID = "<insert_network_id>" # Usually in the following format: "L_00000000"
    SSID = "<insert_ssid_name>" 
    ```

7. Open the `.env` file and add the environment variables:

    ```python
    MERAKI_EMAIL = "<INSERT_MERAKI_EMAIL>"
    MERAKI_PASSWORD = "<INSERT_MERAKI_PASSWORD>"
    MERAKI_API_KEY = "<INSERT_MERAKI_API_KEY>"
    ```

    Note: instead of explicitly defining the environment variables here, you can also export them, for example:

        $ export MERAKI_PASSWORD=INSERT_MERAKI_PASSWORD

## Usage
Now it is time to run the script:

    $ python main.py

This script can be scheduled to run at a fixed cadence, which will result in a new report each time. You can find the CSV report in the folder `csv_reports`.




# Screenshots

![/IMAGES/0image.png](IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.