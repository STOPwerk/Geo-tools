<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd"
	version="1.1.0">
    <!--
    Gemaakt met @@@GeoTools_Online_Url@@@sld_maker
    -->
	<NamedLayer>
		<Name>STOP symbolisatie</Name>
		<UserStyle>
			<Name>verkeersborden_STOP.xml</Name>
<FeatureTypeStyle version="1.1.0" 
    xmlns="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
    <FeatureTypeName>geo:Locatie</FeatureTypeName>
    <SemanticTypeIdentifier>geo:groepID</SemanticTypeIdentifier>
    <Rule>
        <Name>GM0014</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>0</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0034</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>1</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0037</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>2</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0047</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>3</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0059</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>4</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0060</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>5</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0074</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>6</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0080</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>7</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0085</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>8</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0086</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>9</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0090</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>10</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0093</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>11</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0098</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>12</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0106</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>13</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0109</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>14</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0114</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>15</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0118</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>16</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0119</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>17</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0141</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>18</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0147</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>19</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0148</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>20</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0150</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>21</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0153</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>22</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0158</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>23</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0160</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>24</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0163</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>25</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0164</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>26</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0166</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>27</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0168</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>28</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0171</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>29</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0173</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>30</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0175</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>31</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0177</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>32</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0180</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>33</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0183</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>34</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0184</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>35</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0189</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>36</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0193</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>37</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0197</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>38</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0200</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>39</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0202</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>40</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0203</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>41</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0209</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>42</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0213</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>43</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0214</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>44</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0216</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>45</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0221</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>46</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0222</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>47</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0225</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>48</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0226</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>49</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0228</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>50</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0230</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>51</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0232</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>52</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0233</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>53</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0243</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>54</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0244</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>55</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0246</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>56</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0252</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>57</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0262</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>58</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0263</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>59</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0267</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>60</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0268</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>61</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0269</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>62</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0273</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>63</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0274</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>64</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0275</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>65</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0281</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>66</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0285</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>67</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0289</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>68</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0294</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>69</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0296</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>70</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0297</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>71</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0299</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>72</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0301</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>73</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0302</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>74</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0303</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>75</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0307</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>76</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0308</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>77</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0310</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>78</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0312</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>79</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0321</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>80</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0327</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>81</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0331</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>82</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0335</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>83</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0339</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>84</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0340</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>85</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0342</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>86</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0344</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>87</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0345</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>88</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0351</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>89</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0352</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>90</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0353</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>91</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0355</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>92</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0356</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>93</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0358</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>94</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0361</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>95</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0362</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>96</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0363</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>97</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0373</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>98</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0375</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>99</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0376</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>100</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0377</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>101</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0383</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>102</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0384</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>103</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0385</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>104</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0388</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>105</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0392</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>106</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0394</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>107</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0396</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>108</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0397</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>109</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0399</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>110</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0400</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>111</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0402</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>112</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0405</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>113</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0406</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>114</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0415</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>115</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0420</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>116</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0431</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>117</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0432</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>118</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0437</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>119</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0439</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>120</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0441</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>121</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0448</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>122</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0450</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>123</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0451</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>124</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0453</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>125</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0473</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>126</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0479</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>127</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0482</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>128</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0484</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>129</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0489</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>130</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0498</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>131</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0501</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>132</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0503</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>133</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0505</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>134</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0512</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>135</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0513</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>136</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0518</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>137</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0523</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>138</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0530</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>139</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0531</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>140</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0532</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>141</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0534</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>142</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0537</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>143</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0542</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>144</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0546</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>145</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0547</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>146</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0553</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>147</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0556</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>148</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0569</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>149</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0575</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>150</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0579</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>151</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0589</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>152</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0590</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>153</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0597</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>154</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0599</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>155</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0603</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>156</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0606</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>157</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0613</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>158</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0614</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>159</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0622</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>160</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0626</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>161</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0627</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>162</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0629</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>163</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0632</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>164</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0637</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>165</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0638</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>166</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0642</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>167</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0654</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>168</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0664</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>169</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0668</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>170</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0677</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>171</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0678</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>172</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0687</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>173</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0703</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>174</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0715</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>175</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0716</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>176</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0717</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>177</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0718</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>178</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0736</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>179</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0737</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>180</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0743</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>181</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0744</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>182</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0748</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>183</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0753</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>184</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0755</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>185</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0757</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>186</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0758</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>187</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0762</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>188</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0765</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>189</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0766</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>190</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0770</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>191</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0772</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>192</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0777</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>193</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0779</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>194</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0784</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>195</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0785</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>196</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0794</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>197</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0796</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>198</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0797</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>199</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0798</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>200</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0809</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>201</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0820</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>202</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0823</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>203</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0824</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>204</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0826</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>205</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0828</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>206</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0840</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>207</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0845</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>208</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0847</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>209</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0848</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>210</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0851</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>211</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0852</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>212</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0855</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>213</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0858</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>214</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0861</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>215</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0865</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>216</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0866</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>217</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0867</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>218</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0873</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>219</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0879</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>220</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0880</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>221</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0882</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>222</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0888</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>223</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0893</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>224</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0899</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>225</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0907</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>226</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0917</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>227</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0928</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>228</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0935</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>229</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0938</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>230</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0944</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>231</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0946</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>232</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0957</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>233</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0965</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>234</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0971</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>235</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0981</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>236</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0983</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>237</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0984</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>238</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0986</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>239</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0988</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>240</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0994</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>241</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM0995</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>242</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1507</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>243</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1509</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>244</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1525</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>245</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1581</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>246</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1586</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>247</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1598</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>248</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1621</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>249</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1640</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>250</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1641</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>251</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1652</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>252</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1655</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>253</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1658</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>254</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1659</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>255</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1667</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>256</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1669</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>257</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1674</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>258</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1676</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>259</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1680</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>260</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1681</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>261</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1690</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>262</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1695</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>263</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1696</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>264</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1699</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>265</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1700</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>266</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1701</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>267</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1705</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>268</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1706</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>269</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1708</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>270</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1709</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>271</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1711</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>272</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1714</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>273</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1719</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>274</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1721</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>275</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc200</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#000000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1723</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>276</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc201</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebf0d2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1724</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>277</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc202</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#d2ffa5</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1728</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>278</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc203</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b45fd2</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1729</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>279</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc204</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#64aa2d</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1730</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>280</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc205</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffc8be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1731</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>281</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc206</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff3c82</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1734</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>282</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc207</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffa096</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1735</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>283</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc208</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#f091be</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1740</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>284</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc209</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff9b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1742</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>285</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc210</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#28c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1771</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>286</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc211</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff6923</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1773</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>287</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc212</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebc3d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1774</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>288</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc213</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#9b32cd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1783</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>289</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc214</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#dc9b78</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1842</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>290</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc215</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#009b00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1859</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>291</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc216</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82a591</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1876</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>292</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc217</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff78a0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1883</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>293</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc218</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#b9d746</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1884</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>294</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc219</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#82c846</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1892</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>295</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc220</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#cdcdcd</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1894</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>296</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc221</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0000ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1895</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>297</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc222</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00ffff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1896</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>298</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc223</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#afcde1</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1900</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>299</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc224</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#5757ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1901</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>300</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc225</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ff0000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1903</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>301</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc226</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffff00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1904</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>302</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc227</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ffffb4</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1911</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>303</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc228</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#c8a0d7</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1916</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>304</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc229</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#fad2ff</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1924</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>305</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc230</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#ebe1eb</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1926</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>306</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc231</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C02040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1930</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>307</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc232</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E04040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1931</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>308</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc233</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E06060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1940</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>309</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc234</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FF6060</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1942</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>310</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc235</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFC040</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1945</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>311</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc236</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#FFE000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1948</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>312</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc237</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0C0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1949</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>313</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc238</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0A000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1950</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>314</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc239</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1952</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>315</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc240</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#E0E080</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1954</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>316</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc241</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1955</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>317</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc242</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#0080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1959</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>318</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc243</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1960</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>319</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc244</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0E0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1961</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>320</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc245</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1963</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>321</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc246</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#8080FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1966</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>322</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc247</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#C0C0FF</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1969</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>323</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc248</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1970</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>324</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc249</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#40E0C0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1978</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>325</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc250</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#60E0A0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1979</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>326</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc251</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00C000</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1980</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>327</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc252</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#00FF00</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1982</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>328</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc253</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#80FF80</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
    <Rule>
        <Name>GM1991</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>329</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
<PointSymbolizer>
    <Name>pc254</Name>
    <Graphic>
    <Mark>
    <WellKnownName>circle</WellKnownName>
    <Fill>
    <SvgParameter name="fill">#B0B0B0</SvgParameter>
    <SvgParameter name="fill-opacity">1</SvgParameter>
    </Fill>
    <Stroke>
    <SvgParameter name="stroke">#999999</SvgParameter>
    <SvgParameter name="stroke-opacity">0</SvgParameter>
    <SvgParameter name="stroke-width">1</SvgParameter>
    </Stroke>
    </Mark>
    <Size>12</Size>
    <Rotation>0</Rotation>
    </Graphic>
    </PointSymbolizer>
    </Rule>
</FeatureTypeStyle>
		</UserStyle>
	</NamedLayer>
</StyledLayerDescriptor>