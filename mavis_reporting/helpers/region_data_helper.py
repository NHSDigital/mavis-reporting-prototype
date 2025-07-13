from mavis_reporting.models.region import Region
from mavis_reporting.models.provider import Provider
from mavis_reporting.models.school import School


def process_region_data(data: dict) -> Region:
    """
    Process the region data from the API data file and convert it into model instances
    with proper relationships where a region has many providers and a provider has many schools.
    Also establishes back-references from schools to their parent provider and from providers to their parent region.

    Returns:
        Region: A Region instance with its associated providers and schools
    """
    # Create the region instance
    region = Region(data)

    # Initialize providers list for the region
    region.providers = []

    # Process each provider in the region data
    for provider_data in data["providers"]:
        # Create provider instance with back-reference to parent region
        provider = Provider(provider_data, region=region)

        # Initialize schools list for the provider
        provider.schools = []

        # Process each school in the provider data
        for school_data in provider_data["schools"]:
            # Create school instance with back-reference to parent provider
            school = School(school_data, provider=provider)

            # Add school to provider's schools list
            provider.schools.append(school)

        # Add provider to region's providers list
        region.providers.append(provider)

    return region
