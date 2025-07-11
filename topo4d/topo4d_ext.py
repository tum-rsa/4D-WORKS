from pystac.extensions.base import PropertiesExtension, ExtensionManagementMixin, SummariesExtension
import pystac
from pystac.utils import StringEnum, get_required, map_opt
from pyproj import CRS
from pyproj.exceptions import CRSError
from typing import Literal, TypeVar, cast, Any, Generic, Dict, List, Optional
from datetime import datetime


TOPO4D_SCHEMA_URI = "https://stac-extensions.github.io/topo4d/v1.0.0/schema.json"
PREFIX: str = "topo4d:"
DATATYPE_PROP = PREFIX + "data_type"  # required
CRS_PROP = PREFIX + "native_crs" # required
SENSOR_PROP = PREFIX + "sensor" # String
TS_PROP = PREFIX + "tz" # String
ACQUISITION_PROP = PREFIX + "acquisition_mode" # String
DURATION_PROP = PREFIX + "duration"  # Float
TRAJECTORY_PROP = PREFIX + "trajectory"  # Array
SCANPOS_PROP = PREFIX + "scan_position"  # Array
ORIENTATION_PROP = PREFIX + "orientation"  # String
POINTCOUNT_PROP = PREFIX + "point_count" # Integer
SPATIAL_RES_PROP = PREFIX + "spatial_resolution" # Float
MEASUREMENT_ERR_PROP = PREFIX + "measurement_error" # Float
TRAFO_GLOBAL_PROP = PREFIX + "global_trafo" # Array
TRAFO_META_PROP = PREFIX + "trafometa" # Object
PRODUCT_META_PROP = PREFIX + "productmeta" # Object

T = TypeVar("T", pystac.Item, pystac.Asset, pystac.ItemAssetDefinition)

class CRSType:
    def __init__(self, value: str | None):
        if value is None or value.strip().lower() == "undefined" or value.strip() == "":
            self.value = "Undefined"
        elif value.strip().lower() == "local":
            self.value = "Local"
        else:
            try:
                # Validate using pyproj
                _ = CRS.from_user_input(value)
                self.value = value
            except CRSError:
                raise ValueError(f"Invalid CRS string: {value}")
            
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"CRSType({self.value!r})"
    
    def is_defined(self):
        return self.value not in {"Undefined", "Local"}

    def is_local(self):
        return self.value == "Local"

    def is_undefined(self):
        return self.value == "Undefined"
    
    def to_pyproj(self) -> CRS | None:
        if self.is_defined():
            return CRS.from_user_input(self.value)
        return None


class DataType(StringEnum):

    POINTCLOUD = "pointcloud"
    MESH = "mesh"
    RASTER = "raster"
    VECTOR = "vector"
    TEXT = "text"


class TrafoMeta:
    properties: Dict[str, Any]

    def __init__(self, properties: Dict[str, Any]) -> None:
        self.properties = properties

    def apply(
        self,
        reference_epoch: Optional[pystac.Link] = None,
        registration_error: Optional[float] = None,
        transformation: Optional[List[List[float]]] = None,
        affine_transformation: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        translation: Optional[List[float]] = None,
        reduction_point: Optional[List[float]] = None,
    ) -> None:
        
        if reference_epoch is not None:
            self.properties["reference_epoch"] = reference_epoch
        if registration_error is not None:
            self.properties["registration_error"] = registration_error
        if transformation is not None:
            self.properties["transformation"] = transformation
        if affine_transformation is not None:
            self.properties["affine_transformation"] = affine_transformation
        if rotation is not None:
            self.properties["rotation"] = rotation
        if translation is not None:
            self.properties["translation"] = translation
        if reduction_point is not None:
            self.properties["reduction_point"] = reduction_point

    @classmethod
    def create(
        cls,
        reference_epoch: Optional[pystac.Link] = None,
        registration_error: Optional[float] = None,
        transformation: Optional[List[List[float]]] = None,
        affine_transformation: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        translation: Optional[List[float]] = None,
        reduction_point: Optional[List[float]] = None,
    ) -> "TrafoMeta":

        c = cls({})
        c.apply(
            reference_epoch=reference_epoch,
            registration_error=registration_error,
            transformation=transformation,
            affine_transformation=affine_transformation,
            rotation=rotation,
            translation=translation,
            reduction_point=reduction_point,
        )
        return c

    @property
    def reference_epoch(self) -> Optional[pystac.Link]:
        return self.properties.get("reference_epoch")

    @reference_epoch.setter
    def reference_epoch(self, v: pystac.Link) -> None:
        self.properties["reference_epoch"] = v

    @property
    def registration_error(self) -> Optional[float]:
        return self.properties.get("registration_error")

    @registration_error.setter
    def registration_error(self, v: float) -> None:
        self.properties["registration_error"] = v

    @property
    def transformation(self) -> Optional[List[List[float]]]:
        return self.properties.get("transformation")

    @transformation.setter
    def transformation(self, v: List[List[float]]) -> None:
        self.properties["transformation"] = v

    @property
    def affine_transformation(self) -> Optional[List[float]]:
        return self.properties.get("affine_transformation")

    @affine_transformation.setter
    def affine_transformation(self, v: List[float]) -> None:
        self.properties["affine_transformation"] = v

    @property
    def rotation(self) -> Optional[List[float]]:
        return self.properties.get("rotation")

    @rotation.setter
    def rotation(self, v: List[float]) -> None:
        self.properties["rotation"] = v

    @property
    def translation(self) -> Optional[List[float]]:
        return self.properties.get("translation")

    @translation.setter
    def translation(self, v: List[float]) -> None:
        self.properties["translation"] = v

    @property
    def reduction_point(self) -> Optional[List[float]]:
        return self.properties.get("reduction_point")

    @reduction_point.setter
    def reduction_point(self, v: List[float]) -> None:
        self.properties["reduction_point"] = v

    def __repr__(self) -> str:
        return f"<TrafoMeta {self.properties}>"

    def to_dict(self) -> Dict[str, Any]:
        """Returns this metadata as a dictionary."""
        return self.properties


class ProductMeta:
    properties: Dict[str, Any]

    def __init__(self, properties: Dict[str, Any]) -> None:
        self.properties = properties

    def apply(
        self,
        product_name: Optional[str] = None,
        lastupdate: Optional[str] = None,
        param: Optional[Dict[str, Any]] = None,
        derived_from: Optional[pystac.Link] = None,
        product_level: Optional[str] = None,
    ) -> None:
        if product_name is not None:
            self.properties["product_name"] = product_name
        if lastupdate is not None:
            self.properties["lastupdate"] = lastupdate
            self.properties["param"] = param
        if derived_from is not None:
            self.properties["derived_from"] = derived_from
        if product_level is not None:
            self.properties["product_level"] = product_level

    @classmethod
    def create(
        cls,
        product_name: Optional[str] = None,
        lastupdate: Optional[str] = None,
        param: Optional[Dict[str, Any]] = None,
        derived_from: Optional[pystac.Link] = None,
        product_level: Optional[str] = None,
    ) -> "ProductMeta":
        c = cls({})
        c.apply(
            product_name=product_name,
            lastupdate=lastupdate,
            param=param,
            derived_from=derived_from,
            product_level=product_level,
        )
        return c

    @property
    def product_name(self) -> str:
        return get_required(self.properties.get("product_name"), self, "product_name")

    @product_name.setter
    def product_name(self, v: str) -> None:
        self.properties["product_name"] = v

    @property
    def lastupdate(self) -> Optional[datetime]:
        val = self.properties.get("lastupdate")
        return datetime.fromisoformat(val) if val else None

    @lastupdate.setter
    def lastupdate(self, v: str) -> None:
        self.properties["lastupdate"] = v

    @property
    def param(self) -> Optional[Dict[str, Any]]:
        return self.properties.get("param")

    @param.setter
    def param(self, v: Dict[str, Any]) -> None:
        self.properties["param"] = v

    @property
    def derived_from(self) -> Optional[pystac.Link]:
        return self.properties.get("derived_from")

    @derived_from.setter
    def derived_from(self, v: pystac.Link) -> None:
        self.properties["derived_from"] = v

    @property
    def product_level(self) -> Optional[str]:
        return self.properties.get("product_level")

    @product_level.setter
    def product_level(self, v: str) -> None:
        self.properties["product_level"] = v

    def __repr__(self) -> str:
        return "<ProductMeta {}>".format(self.properties)

    def to_dict(self) -> Dict[str, Any]:
        return self.properties


class Topo4DExtension(
    PropertiesExtension, ExtensionManagementMixin
    ):
    name: Literal["topo4d"] = "topo4d"

    def __init__(self, item: T):
        self.item = item
        self.properties = item.properties

    def apply(
        self,
        data_type: DataType | str | None = None,
        native_crs: CRSType | str | None = None,
        sensor: str | None = None,
        tz: str | None = None,
        acquisition_mode: str | None = None,
        duration: float | None = None, 
        trajectory: list | None = None,
        scan_position: list | None = None,
        orientation: str | None = None,
        point_count: int | None = None,
        spatial_resolution: float | None = None,
        measurement_error: float | None = None,
        global_trafo: list | None = None,
        trafometa: TrafoMeta| dict | None = None,
        productmeta: ProductMeta | dict | None = None

    ):
        """Applies the extension to the item."""
        if TOPO4D_SCHEMA_URI not in self.item.stac_extensions:
            self.item.stac_extensions.append(TOPO4D_SCHEMA_URI)

        self.data_type = data_type
        self.native_crs = native_crs
        self.sensor = sensor
        self.tz = tz
        self.acquisition_mode = acquisition_mode
        self.duration = duration
        self.trajectory = trajectory
        self.scan_position = scan_position
        self.orientation = orientation
        self.point_count = point_count
        self.spatial_resolution = spatial_resolution
        self.measurement_error = measurement_error
        self.global_trafo = global_trafo
        self.trafometa = trafometa
        self.productmeta = productmeta

    ######################################### Required Properties #########################################
    @property
    def native_crs(self) -> CRSType | None:
        return get_required(self._get_property(CRS_PROP, str), self, CRS_PROP)

    @native_crs.setter
    def native_crs(self, v: CRSType | str | None):
        if isinstance(v, CRSType):
            crs_str = str(v)
        elif isinstance(v, str) or v is None:
            crs_str = str(CRSType(v))
        else:
            raise TypeError(f"native_crs must be CRSType, str, or None — got {type(v)}")

        self._set_property(CRS_PROP, crs_str)

    @property
    def data_type(self) -> DataType:
        return get_required(self._get_property(DATATYPE_PROP, str), self, DATATYPE_PROP)
    
    @data_type.setter
    def data_type(self, v: DataType | str | None):
        if isinstance(v, DataType):
            self._set_property(DATATYPE_PROP, v.value)
        elif isinstance(v, str):
            self._set_property(DATATYPE_PROP, DataType(v).value)
        elif v is None:
            self._set_property(DATATYPE_PROP, None)
        else:
            raise TypeError(f"data_type must be DataType, str, or None — got {type(v)}")


    ########################################## Optional Properties #########################################
    @property
    def sensor(self) -> str:
        return self.properties.get(SENSOR_PROP)
    
    @sensor.setter
    def sensor(self, v: str | None):
        self._set_property(SENSOR_PROP, v, pop_if_none=True)

    @property
    def tz(self) -> str | None:
        return self.properties.get(TS_PROP)
    
    @tz.setter
    def tz(self, v: str | None):
        self._set_property(TS_PROP, v, pop_if_none=True)

    @property
    def acquisition_mode(self) -> str | None:
        return self.properties.get(ACQUISITION_PROP)
    
    @acquisition_mode.setter
    def acquisition_mode(self, v: str | None):
        self._set_property(ACQUISITION_PROP, v, pop_if_none=True)

    @property
    def duration(self) -> float | None:
        return self.properties.get(DURATION_PROP)
    
    @duration.setter
    def duration(self, v: float | None):
        self._set_property(DURATION_PROP, v, pop_if_none=True)


    @property
    def trajectory(self) -> list | None:
        return self.properties.get(TRAJECTORY_PROP)
    
    @trajectory.setter
    def trajectory(self, v: list | None):
        self._set_property(TRAJECTORY_PROP, v, pop_if_none=True)


    @property
    def scan_position(self) -> list | None:
        return self.properties.get(SCANPOS_PROP)
    
    @scan_position.setter
    def scan_position(self, v: list | None):
        self._set_property(SCANPOS_PROP, v, pop_if_none=True)


    @property
    def orientation(self) -> str | None:
        return self.properties.get(ORIENTATION_PROP)
    
    @orientation.setter
    def orientation(self, v: str | None):
        self._set_property(ORIENTATION_PROP, v, pop_if_none=True)


    @property
    def point_count(self) -> int | None:
        return self.properties.get(POINTCOUNT_PROP)
    
    @point_count.setter
    def point_count(self, v: int | None):
        self._set_property(POINTCOUNT_PROP, v, pop_if_none=True)


    @property
    def spatial_resolution(self) -> float | None:
        return self.properties.get(SPATIAL_RES_PROP)
    
    @spatial_resolution.setter
    def spatial_resolution(self, v: float | None):
        self._set_property(SPATIAL_RES_PROP, v, pop_if_none=True)


    @property
    def measurement_error(self) -> float | None:
        return self.properties.get(MEASUREMENT_ERR_PROP)
    
    @measurement_error.setter
    def measurement_error(self, v: float | None):
        self._set_property(MEASUREMENT_ERR_PROP, v, pop_if_none=True)

    @property
    def global_trafo(self) -> list | None:
        return self.properties.get(TRAFO_GLOBAL_PROP)
    
    @global_trafo.setter
    def global_trafo(self, v: list | None):
        self._set_property(TRAFO_GLOBAL_PROP, v, pop_if_none=True)


    @property
    def trafometa(self) -> TrafoMeta | dict | None:
        return self.properties.get(TRAFO_META_PROP)
    
    @trafometa.setter
    def trafometa(self, v: TrafoMeta | dict | None):
        self._set_property(TRAFO_META_PROP, v.to_dict(), pop_if_none=True)

    @property
    def productmeta(self) -> ProductMeta | dict | None:
        return self.properties.get(PRODUCT_META_PROP)
    
    @productmeta.setter
    def productmeta(self, v: ProductMeta | dict | None):
        self._set_property(PRODUCT_META_PROP, v.to_dict(), pop_if_none=True)

    @classmethod
    def get_schema_uri(cls) -> str:
        return TOPO4D_SCHEMA_URI

    # @classmethod
    # def add_to(cls, item: Item) -> "Topo4DExtension":
    #     item.stac_extensions.append(TOPO4D_SCHEMA_URI)
    #     return cls(item)

    @classmethod
    def ext(cls, item: T, add_if_missing: bool = False):
        if isinstance(item, pystac.Item):
            cls.ensure_has_extension(item, add_if_missing)
            return Topo4DExtension(item)
        else:
            raise pystac.ExtensionTypeError(cls._ext_error_message(item))
